
        document.addEventListener("DOMContentLoaded", function () {
            const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
            const token = localStorage.getItem('token');
            const baseUrl = "{{ base_url }}";
            // const marksheets = 
            const swalWithBootstrapButtons = Swal.mixin({
                customClass: {
                    confirmButton: "btn btn-success",
                    cancelButton: "btn btn-danger"
                },
                buttonsStyling: false
            });

            window.destroy = function destroy(eNo) {

                swalWithBootstrapButtons.fire({
                    title: "Are you sure?",
                    text: "You won't be able to revert this!",
                    icon: "warning",
                    showCancelButton: true,
                    confirmButtonText: "Yes, delete it!",
                    cancelButtonText: "No, cancel!",
                    reverseButtons: true
                }).then((result) => {
                    if (result.isConfirmed) {
                        fetch(`${baseUrl}delete_student/`, {
                            method: "POST",
                            headers: {
                                'X-CSRFToken': csrfToken,
                                "Content-type": "application/json; charset=UTF-8"
                            },
                            body: JSON.stringify({
                                "enrollment_no": eNo,
                                "token": token,
                            })
                        }).then(response => {
                            if (response.ok) {
                                swalWithBootstrapButtons.fire({
                                    title: "Deleted!",
                                    text: "Student has been deleted.",
                                    icon: "success"
                                }).then(response => {
                                    location.reload();
                                });
                            } else {
                                swalWithBootstrapButtons.fire({
                                    title: "Error!",
                                    text: "There was an issue deleting student.",
                                    icon: "error"
                                });
                            }
                        }).catch(error => {
                            console.error("Error:", error);
                            swalWithBootstrapButtons.fire({
                                title: "Error!",
                                text: "There was an issue deleting student.",
                                icon: "error"
                            });
                        });
                    } else if (result.dismiss === Swal.DismissReason.cancel) {
                        swalWithBootstrapButtons.fire({
                            title: "Cancelled",
                            text: "Your imaginary file is safe :)",
                            icon: "error"
                        });
                    }
                });
            };
        });


        document.addEventListener("DOMContentLoaded", function () {
            addMarkSheet();
            var data = "{{ admin_info.students }}";
            var btns = document.getElementsByClassName("text-center");

            if (data.length > 10) {
                for (var i = 0; i < btns.length; i++) {
                    btns[i].style.display = "block";
                }
            } else {
                for (var i = 0; i < btns.length; i++) {
                    btns[i].style.display = "none";
                }
            }
        });
        function cancelUpdate(enrollmentNo) {
            $('.modal-backdrop').remove();
        }

        let marksheetCounter = 0;

        function addMarkSheet() {

            var marksheetList = document.getElementById("marksheetList");
            if (!marksheetList) {
                console.error("Element with id 'marksheetList' not found.");
                return;
            }
            marksheetCounter++;

            var newMarkSheetDiv = document.createElement("div");
            newMarkSheetDiv.className = "row mb-3 marksheets-class";

            newMarkSheetDiv.innerHTML = `
            <div class="col-md-4">
                <div class="form-group">
                    <label class="required-field-name" for="session">Session</label>
                    <input type="text" class="form-control required-field" id="session" name="session" placeholder="Enter Session">
                </div>
                <div class="form-group">
                    <label class="required-field-name" for="semester">Semester</label>
                    <input type="text" class="form-control required-field" id="semester" name="semester" placeholder="Enter Semester">
                </div>
            </div>
            <div class="col-md-4">
                <div class="form-group">
                    <label class="required-field-name" for="sgpa">SGPA</label>
                    <input type="text" class="form-control required-field" id="sgpa" name="sgpa" placeholder="Enter SGPA">
                </div>
                <div class="form-group">
                    <label class="required-field-name" for="status">Status</label>
                    <input type="text" class="form-control required-field" id="status" name="status" placeholder="Enter Status">
                </div>
            </div>
            <div class="col-md-4">
                <div class="form-group">
                    <label class="required-field-name" for="result">Result</label>
                    <input type="text" class="form-control required-field" id="result" name="result" placeholder="Enter Result">
                </div>
                <div class="form-group d-block">
                    <label class="required-field-name" for="file">Marksheet Upload</label>
                    <input type="file" class="form-control-file required-field" id="file" name="marksheet">
                </div>

            </div>
            
        `;
            marksheetList.appendChild(newMarkSheetDiv);
        }

        async function extractAndDisplayData(event) {

            var isLoading = document.getElementById("loader");
            var overlay = document.getElementById("loader-overlay");
            isLoading.style.display = "block";
            overlay.style.display = "block";


            const studentUrl = "{{ api_url }}students/";
            const markSheetUrl = "{{ api_url }}marksheets/";
            const studentDataUrl = "{{ api_url }}student-data/";
            const addStudentUrl = "{{ api_url }}add-student/";
            const token = localStorage.getItem('token');
            var dataInserted = false;


            const fetchWithAuth = (url, method, body, isJson = false) => {
                return fetch(url, {
                    method: method,
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        ...(isJson && { 'Content-Type': 'application/json' })
                    },
                    body: body
                })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        } else {
                            if (url == addStudentUrl) {
                                dataInserted = true;
                            }
                        }

                        return response.json();
                    });
            };

            try {

                const studentData = {
                    "center_id": 1,
                    "enrollment_no": document.querySelector('#enrollment_no').value,
                    "profile_pic": document.querySelector('#profile_pic').files[0],
                    "full_name": document.querySelector('#full_name').value,
                    "password": document.querySelector('#password').value,
                    "father_name": document.querySelector('#father_name').value,
                    "mother_name": document.querySelector('#mother_name').value,
                    "gender": document.querySelector('#gender').value,
                    "date_of_birth": document.querySelector('#date_of_birth').value,
                    "category": document.querySelector('#category').value,
                    "email": document.querySelector('#email').value,
                    "mobile_number": document.querySelector('#mobile_number').value,
                    "address": document.querySelector('#address').value,
                };

                // Add mark sheet
                const marksheetData = {
                    "student_enrollment_no": studentData.enrollment_no,
                    "session": document.querySelector('#session').value,
                    "semester": document.querySelector('#semester').value,
                    "sgpa": document.querySelector('#sgpa').value,
                    "status": document.querySelector('#status').value,
                    "result": document.querySelector('#result').value,
                    "file": document.querySelector('#file').files[0],
                };

                const marksheetFormData = new FormData();
                Object.entries(marksheetData).forEach(([key, value]) => marksheetFormData.append(key, value));

                const marksheetResponse = await fetchWithAuth(
                    markSheetUrl,
                    'POST',
                    marksheetFormData,
                );
                console.log('Mark sheet added:', marksheetResponse);

                // Extract id_list from marksheetResponse
                const idList = marksheetResponse.id_list;

                // Add student
                studentData.list_of_interests = idList;

                const studentFormData = new FormData();
                Object.entries(studentData).forEach(([key, value]) => studentFormData.append(key, value));

                const studentResponse = await fetchWithAuth(studentUrl, 'POST', studentFormData,);
                console.log('Student added:', studentResponse);

                // Add student data
                const studentDoc = {
                    "student_enrollment_no": studentData.enrollment_no,
                    "student_provision": document.querySelector('#provision').files[0],
                    "student_admit_card": document.querySelector('#admit_card').files[0],
                    "student_affidevit": document.querySelector('#affidevit').files[0],
                    "student_migrations": document.querySelector('#migration').files[0],
                };

                const formDetails = new FormData();
                Object.entries(studentDoc).forEach(([key, value]) => formDetails.append(key, value));

                const studentDataResponse = await fetchWithAuth(studentDataUrl, 'POST', formDetails);
                console.log('Student data added:', studentDataResponse);

                // Add student credentials
                const addStudentPayload = {
                    "username": studentData.enrollment_no,
                    "password": studentData.password
                };

                const addStudentResponse = await fetchWithAuth(addStudentUrl, 'POST', JSON.stringify(addStudentPayload), true,);
                console.log('Student credentials added:', addStudentResponse);

                if (dataInserted) {
                    isLoading.style.display = 'none';
                    overlay.style.display = 'none';
                    Swal.fire({
                        title: "Student Enrolled",
                        text: "Student Added Successfully",
                        icon: "success"
                    }).then(response => {
                        location.reload();
                    });
                    $('#editModal').modal('hide');
                }
            } catch (error) {
                console.log(error);
                overlay.style.display = 'none';
                isLoading.style.display = 'none';
                Swal.fire({
                    title: "Oops...",
                    text: "Student Not Added",
                    icon: "error"
                });
                console.error('There was a problem with the fetch operation:', error);
            }
        }


        function removeMarkSheet(button) {
            var marksheetDiv = button.parentElement.parentElement;
            marksheetCounter--;
            marksheetDiv.remove();
        }

        function filterTable(columnIndex, filterValue) {
            var table = document.querySelector('.table');
            var rows = table.getElementsByTagName('tr');
            for (var i = 1; i < rows.length; i++) {
                var cells = rows[i].getElementsByTagName('td');
                var cell = cells[columnIndex];
                if (cell.textContent.trim() === filterValue || filterValue === "") {
                    rows[i].style.display = "";
                } else {
                    rows[i].style.display = "none";
                }
            }
        }

        var currentPage = 0;
        var rowsPerPage = 10;

        // Function to show rows for the current page
        function showRows() {
            var table = document.querySelector('.table');
            var tr = table.getElementsByTagName('tr');
            var startIndex = currentPage * rowsPerPage + 1;
            var endIndex = (currentPage + 1) * rowsPerPage + 1;
            for (var i = 1; i < tr.length; i++) {
                if (i >= startIndex && i < endIndex) {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            }
        }

        // Function to go to the previous page
        function prevPage() {
            if (currentPage > 0) {
                currentPage--;
                showRows();
                updatePageNumbers();
            }
        }

        // Function to go to the next page
        function nextPage() {
            var table = document.querySelector('.table');
            var tr = table.getElementsByTagName('tr');
            var totalPages = Math.ceil((tr.length - 1) / rowsPerPage);
            if (currentPage < totalPages - 1) {
                currentPage++;
                showRows();
                updatePageNumbers();
            }
        }

        // Function to update the displayed page numbers
        function updatePageNumbers() {
            var table = document.querySelector('.table');
            var tr = table.getElementsByTagName('tr');
            var totalPages = Math.ceil((tr.length - 1) / rowsPerPage);
            var pageNumbers = document.getElementById("page-numbers");
            pageNumbers.innerHTML = "";

            var startPage = 0;
            var endPage = totalPages - 1;
            if (totalPages > 5) {
                startPage = Math.max(currentPage - 2, 0);
                endPage = Math.min(currentPage + 2, totalPages - 1);
                if (endPage - startPage < 4) {
                    if (startPage === 0) {
                        endPage = Math.min(startPage + 4, totalPages - 1);
                    } else {
                        startPage = Math.max(endPage - 4, 0);
                    }
                }
                if (startPage > 0) {
                    pageNumbers.appendChild(createPageNumberButton(0));
                    if (startPage > 1) {
                        pageNumbers.appendChild(createEllipsis());
                    }
                }
            }

            for (var i = startPage; i <= endPage; i++) {
                pageNumbers.appendChild(createPageNumberButton(i));
            }

            if (endPage < totalPages - 1) {
                if (endPage < totalPages - 2) {
                    pageNumbers.appendChild(createEllipsis());
                }
                pageNumbers.appendChild(createPageNumberButton(totalPages - 1));
            }
        }

        // Function to create a page number button
        function createPageNumberButton(page) {
            var button = document.createElement("button");
            button.className = "m-1 btn btn-secondary";
            button.textContent = page + 1;
            if (page === currentPage) {
                button.classList.add("active");
            }
            button.onclick = function () {
                currentPage = page;
                showRows();
                updatePageNumbers();
            };
            return button;
        }

        // Function to create an ellipsis element
        function createEllipsis() {
            var ellipsis = document.createElement("span");
            ellipsis.textContent = "...";
            return ellipsis;
        }

        // Initial call to show rows for the first page and update page numbers
        showRows();
        updatePageNumbers();