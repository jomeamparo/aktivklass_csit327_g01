window.uploadedStudents = JSON.parse(
    document.getElementById("uploaded-data-json").textContent
  );
  
  const openModalBtn = document.getElementById("openModalBtn");
  const addStudentModal = document.getElementById("addStudentModal");
  const closeModalBtn = document.getElementById("closeModalBtn");
  const searchBtn = document.getElementById("searchBtn");
  const clearBtn = document.getElementById("clearBtn");
  const searchInput = document.getElementById("searchInput");
  const searchResults = document.getElementById("searchResults");
  
  const excelPreviewModal = document.getElementById("excelPreviewModal");
  const closeExcelModalBtn = document.getElementById("closeExcelModalBtn");
  const saveStudentListBtn = document.getElementById("saveStudentListBtn");
  
  const studentsContainer = document.getElementById("studentsContainer");
  let studentsList = document.getElementById("studentsList");
  const noStudentsMsg = document.getElementById("noStudentsMsg");
  
  const selectedSubjectCode = document.getElementById("subjectCode").textContent;
  
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  
  function createStudentListItem(student) {
    const li = document.createElement("li");
    li.className = "py-2";
    li.setAttribute("data-student-id", student.id);
    li.textContent = `(${student.student_id}) - ${student.last_name}, ${student.first_name} ${student.middle_name || ''}`;
    return li;
  }
  
  openModalBtn.addEventListener("click", () => {
    addStudentModal.classList.remove("hidden");
    searchInput.value = "";
    searchResults.innerHTML = '<p class="text-center text-gray-500 italic">Type in the search area to search the student</p>';
    searchInput.focus();
  });
  
  closeModalBtn.addEventListener("click", () => {
    addStudentModal.classList.add("hidden");
  });
  
  clearBtn.addEventListener("click", () => {
    searchInput.value = "";
    searchResults.innerHTML = '<p class="text-center text-gray-500 italic">Type in the search area to search the student</p>';
    searchInput.focus();
  });
  
  searchBtn.addEventListener("click", () => {
    const query = searchInput.value.trim();
    if (!query) {
      searchResults.innerHTML = '<p class="text-center text-gray-500 italic">Type in the search area to search the student</p>';
      return;
    }
  
    fetch(`/class_record/search_students?q=${encodeURIComponent(query)}`)
      .then((response) => response.json())
      .then((data) => {
        const students = data.students;
        if (!students.length) {
          searchResults.innerHTML = '<p class="text-center text-gray-500 italic">No students found.</p>';
          return;
        }
  
        searchResults.innerHTML = "";
        students.forEach((student) => {
          const div = document.createElement("div");
          div.className = "py-1 px-2 hover:bg-gray-100 cursor-pointer rounded";
          div.textContent = `(${student.student_id}) - ${student.last_name}, ${student.first_name} ${student.middle_name || ""}`;
          div.dataset.studentId = student.id;
  
          div.addEventListener("click", () => {
            if (studentsList) {
              if (studentsList.querySelector(`[data-student-id="${student.id}"]`)) {
                alert("Student already in the list.");
                return;
              }
            } else {
              studentsList = document.createElement("ul");
              studentsList.id = "studentsList";
              studentsList.className = "divide-y divide-gray-200 max-h-96 overflow-y-auto";
              studentsContainer.appendChild(studentsList);
              if (noStudentsMsg) noStudentsMsg.style.display = "none";
            }
  
            // Save to Enrollment table using student_id and subject_code
            fetch("/class_record/enroll-student/", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
              },
              body: JSON.stringify({
                student_id: student.student_id,
                subject_code: selectedSubjectCode,
              }),
            })
              .then((response) => {
                if (!response.ok) {
                  throw new Error("Enrollment failed.");
                }
                return response.json();
              })
              .then(() => {
                const li = createStudentListItem(student);
                studentsList.appendChild(li);
                addStudentModal.classList.add("hidden");
              })
              .catch((error) => {
                alert(error.message);
              });
          });
  
          searchResults.appendChild(div);
        });
      })
      .catch(() => {
        searchResults.innerHTML = '<p class="text-center text-red-500 italic">Error searching students.</p>';
      });
  });
  
  const enrolledCount = {{ enrolled|length|default:0 }};
  const unenrolledCount = {{ unenrolled|length|default:0 }};
  
  const hasEnrolledStudents = enrolledCount > 0;
  const hasUnenrolledStudents = unenrolledCount > 0;
  
  if (hasEnrolledStudents || hasUnenrolledStudents) {
    excelPreviewModal.classList.remove("hidden");
  }
  
  closeExcelModalBtn.addEventListener("click", () => {
    excelPreviewModal.classList.add("hidden");
  
    fetch("{% url 'clear_uploaded_students_session' %}", {
      method: "POST",
      headers: { "X-CSRFToken": "{{ csrf_token }}" },
    });
  });
  
  saveStudentListBtn.addEventListener("click", () => {
    if (enrolledCount === 0) {
      alert("No students to save.");
      return;
    }
  
    saveStudentListBtn.disabled = true;
    saveStudentListBtn.textContent = "Saving...";
  
    const studentsToSave = [
      ...(window.uploadedStudents.enrolled || []),
      ...(window.uploadedStudents.unenrolled || []),
    ];
  
    fetch("{% url 'save_uploaded_students_to_class' class.id %}", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": "{{ csrf_token }}",
      },
      body: JSON.stringify({ students: studentsToSave }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          alert("Students saved successfully!");
          window.location.reload();
        } else {
          alert("Error saving students: " + (data.error || "Unknown error"));
        }
      })
      .catch(() => alert("Network error saving students."))
      .finally(() => {
        saveStudentListBtn.disabled = false;
        saveStudentListBtn.textContent = "Save";
      });
  });
  
  const container = document.getElementById("handsontable-container");
  
  const studentsData = [
    {% for student in students %}
    ["{{ student.last_name }}, {{ student.first_name }} {{ student.middle_name }}", "{{ student.student_id }}"],
    {% endfor %}
  ];
  
  const initial_data = studentsData.map((row) => {
    // Fill with empty grades
    return row.concat(new Array(24).fill(""));
  });
  
  const hot = new Handsontable(container, {
    data: initial_data,
    nestedHeaders: [
      [
        { label: "", colspan: 2 },
        { label: "Quizzes", colspan: 5 },
        { label: "Assignments", colspan: 5 },
        { label: "Seatworks", colspan: 5 },
        { label: "Laboratory Works", colspan: 5 },
        { label: "PE", colspan: 1 },
        { label: "ME", colspan: 1 },
        { label: "PFE", colspan: 1 },
        { label: "FE", colspan: 1 },
        { label: "Remarks", colspan: 1 },
      ],
      [
        { label: "", colspan: 2 },
        ...Array(4)
          .fill()
          .flatMap(() => ["1", "2", "3", "4", "5"].map((n) => ({ label: n, colspan: 1 }))),
        null,
        null,
        null,
        null,
        null,
      ],
      [
        "Student Name",
        "ID Number",
        "Quiz 1",
        "Quiz 2",
        "Quiz 3",
        "Quiz 4",
        "Quiz 5",
        "Assign 1",
        "Assign 2",
        "Assign 3",
        "Assign 4",
        "Assign 5",
        "SW 1",
        "SW 2",
        "SW 3",
        "SW 4",
        "SW 5",
        "Lab 1",
        "Lab 2",
        "Lab 3",
        "Lab 4",
        "Lab 5",
        "PE",
        "ME",
        "PFE",
        "FE",
        "Remarks",
      ],
    ],
    licenseKey: "non-commercial-and-evaluation",
    colWidths: 100,
    width: "100%",
    rowHeaders: true,
    colHeaders: true,
    manualColumnFreeze: true,
    fixedColumnsStart: 2,
    autoWrapRow: true,
    autoWrapCol: true,
    cells: (row, col) => {
      const cell = {};
      if (col === 0 || col === 1) {
        cell.readOnly = true;
      }
      return cell;
    },
    contextMenu: {
      items: {
        freezeColumn: {
          name: "Freeze this column",
          disabled: function () {
            const selectedColumn = this.getSelectedRangeLast()?.from?.col;
            return selectedColumn !== 0;
          },
        },
        unfreezeColumn: {
          name: "Unfreeze this column",
          disabled: function () {
            const selectedColumn = this.getSelectedRangeLast()?.from?.col;
            return selectedColumn !== 0;
          },
        },
        separator: Handsontable.plugins.ContextMenu.SEPARATOR,
        copy: { name: "Copy" },
        paste: { name: "Paste" },
      },
    },
  });
  