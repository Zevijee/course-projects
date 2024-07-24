import todoMantras from './mantras.js';

document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('indexIdentifier')) {
        loadIndexPage()
    } else if (document.getElementById('create-future-list-identifier')) {
        loadCreateFuture()
    } else if (document.getElementById('passed-list')) {
        loadPassed()
    }
});

function loadPassed() {
    const date = document.querySelector('#date').value;


    var yesterday = new Date()
    yesterday.setDate(yesterday.getDate() - 1)

    $(document).ready(function() {
        $('#datepicker').datepicker({
          format: 'yyyy-mm-dd',
          beforeShowDay: function(date) {
            // Disable future dates
            if (date > yesterday) {
              return {
                enabled: false
              };
            }
            return {
              enabled: true
            };
          }
        });
      });

    document.querySelector('#see-past-list').addEventListener('click', function() {
        setTimeout(function() {
            $('#datepicker').datepicker('show');
        }, 0);
    });

    $(document).on('change', '#datepicker', function() {
        const selectedDate = $(this).val();

        const pathname = window.location.pathname;
        const newURL = pathname.substring(0, pathname.lastIndexOf('/') + 1) + selectedDate;

        window.location.href = newURL;
    });

    loadTasks(date, true);
}

function loadCreateFuture() {
    $(document).ready(function() {
        var tommorow = new Date();
        tommorow.setDate(tommorow.getDate() + 1)

        $('#datepicker').datepicker({
            format: 'yyyy-mm-dd',
            startDate: tommorow
        });
    })

    const date = document.querySelector('#date').value;

    document.querySelector('#todays-tasks').addEventListener('click', function(event) {
        const target = event.target;

        if (target.matches('.edit')) {
            const editedTask = window.prompt('Edit task here:', target.dataset.text);
            markCompleteEdit(target.dataset.task, 'edit', editedTask, date);
        } else if (target.matches('.delete')) {
            markCompleteEdit(target.dataset.task, 'delete', null, date)
        }
    })

    document.querySelector('#new_task').addEventListener('submit', function(event) {
        event.preventDefault();

        var form = event.target;
        var formData = new FormData(form);

        createNewTask(formData, date)
    })

    document.querySelector('#create-a-future-list').addEventListener('click', function() {
        setTimeout(function() {
            $('#datepicker').datepicker('show');
        }, 0);
    });

    $(document).on('change', '#datepicker', function() {
        const selectedDate = $(this).val();

        const pathname = window.location.pathname;
        const newURL = pathname.substring(0, pathname.lastIndexOf('/') + 1) + selectedDate;

        window.location.href = newURL;
    });

    loadTasks(date);
};

function loadIndexPage(){
    $(document).ready(function() {
        var tommorow = new Date();
        tommorow.setDate(tommorow.getDate() + 1)

        $('#datepicker-future').datepicker({
            format: 'yyyy-mm-dd',
            startDate: tommorow
        });

        var yesterday = new Date()
        yesterday.setDate(yesterday.getDate() - 1)

        $(document).ready(function() {
            $('#datepicker-past').datepicker({
              format: 'yyyy-mm-dd',
              beforeShowDay: function(date) {
                // Disable future dates
                if (date > yesterday) {
                  return {
                    enabled: false
                  };
                }
                return {
                  enabled: true
                };
              }
            });
          });

    });


    setGreetingDateAndMantra()

    document.querySelector('#new_task').addEventListener('submit', function(event) {
        event.preventDefault();

        var form = event.target;
        var formData = new FormData(form);

        createNewTask(formData, 'today')
    })

    document.querySelector('#todays-tasks').addEventListener('click', function(event) {
        const target = event.target;

        if (target.matches('.edit')) {
            const editedTask = window.prompt('Edit task here:', target.dataset.text);
            markCompleteEdit(target.dataset.task, 'edit', editedTask, 'today');
        } else if (target.matches('#mark-complete')) {
            markCompleteEdit(target.dataset.task, 'complete', null, 'today');
        } else if (target.matches('.delete')) {
            markCompleteEdit(target.dataset.task, 'delete', null, 'today');
        }
    })

    document.querySelector('#create-a-future-list').addEventListener('click', function() {
        setTimeout(function() {
            $('#datepicker-future').datepicker('show');
        }, 0);
    });

    document.querySelector('#see-past-list').addEventListener('click', function() {
        setTimeout(function() {
            $('#datepicker-past').datepicker('show');
        }, 0);
    });


    $(document).on('change', '#datepicker-future', function() {
        const selectedDate = $(this).val();
        $('#datepicker').datepicker('hide');
        window.location.href = `create_future_list/${selectedDate}`
    });


    $(document).on('change', '#datepicker-past', function() {
        const selectedDate = $(this).val();
        $('#datepicker').datepicker('hide');
        window.location.href = `see_passed_list/${selectedDate}`
    });

    loadTasks('today');

}


function setGreetingDateAndMantra() {
    var date = new Date();

    // checking what time of day it is and setting it for the greeting
    var hours = date.getHours();

    var timeOfDay
    if (hours < 12){
        timeOfDay = 'Morning';
    } else if (hours < 18) {
        timeOfDay = 'Afternoon';
    } else {
        timeOfDay = 'Evening';
    };

    document.querySelector('#time-of-day').textContent = timeOfDay;

    // setting the date
    var dateStr = date.toLocaleDateString();

    document.querySelector('#date').innerHTML = dateStr;

    // setting the mantra
    const randomIndex = Math.floor(Math.random() * todoMantras.length);
    const mantra = todoMantras[randomIndex];

    document.querySelector('#mantra').innerHTML = mantra;
}

function createNewTask(formData, dayToDo) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // extract the data
    const task = formData.get('task');
    const time = formData.get('time');
    const urgency = formData.get('urgency');

    if (task === ''){
        alert('The task box must contain a task.');
        return;
    }

    // call a fetch on the api
    fetch('/create_task', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body:JSON.stringify({
            task: task,
            time: time,
            dayToDo: dayToDo,
            urgency: urgency
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message)
        loadTasks(dayToDo)
    })
    .catch(error => console.error('Error:', error));

    document.querySelector('#new_task').reset();
}

function loadTasks(list, past){
    fetch(`/load_tasks/${list}`)
    .then(response => response.json())
    .then(data => {

        const responsedList = data.list;
        const todaysTasksDiv = document.querySelector('#todays-tasks');

        todaysTasksDiv.innerHTML = '';

        if (responsedList.length === 0){
            const message = document.createElement('p');
            message.textContent = 'You dont have any tasks for today. You should create some.'
            todaysTasksDiv.append(message);
        }


        let taskNumber = 1;

        responsedList.forEach(task => {
            const taskId = task.id;
            const text = task.text;
            const time = task.time.split(':').slice(0, 2).join(':');
            const urgency = task.urgency;
            const completed = task.completed;

            let [hour, minute] = time.split(':');

            let halfTime = new Date;
            halfTime.setHours(hour);
            halfTime.setMinutes(minute);

            let fullTime = halfTime.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true });

            const taskDiv = document.createElement('div');
            taskDiv.className = 'task-div';

            let checkBox = '';
            let completeMessage  = '';

            if (list === 'today') {
                checkBox = `<input type="checkbox" id="mark-complete" data-task="${task.id}" ${completed ? 'checked' : ''}><label for="mark-complete">Completed</label>`;
            };

            if (past) {
                if (completed){
                    completeMessage = 'This task was completed!!! :-)'
                } else {
                    completeMessage = 'This task was not completed. :-('
                }
            };

            const deleteBtn = past ? '' : `<button class="btn btn-primary delete" data-task="${task.id}">Delete Task</button>`;
            const editLink = past ? '' : `<br><a class="edit" href="#" data-task="${taskId}" data-text="${text}">edit</a>`;

            taskDiv.innerHTML = `
                <h3>Task #${taskNumber}.</h3>
                <strong>Todo:</strong> ${text}
                ${editLink}
                <br>
                <strong>do task at:</strong> ${fullTime}
                <br>
                <strong>urgency:</strong> ${urgency}
                <br>
                ${checkBox}
                ${deleteBtn}
                <strong>${completeMessage}</strong>
                <hr>
            `;

            taskNumber++;

            todaysTasksDiv.append(taskDiv);
        })
    })
};

function markCompleteEdit(task, action, editedTask, date) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch('/edit_and_complete_task', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            task: task,
            action: action,
            editedTask: editedTask
        })
    })
    .then(response => response.json())
    .then(data => {
        loadTasks(date)
        console.log(data.message)
    })
};
