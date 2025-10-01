// app.js

document.addEventListener('DOMContentLoaded', () => {
    // ... (nenhuma mudança no topo do arquivo, até a função addTaskForm) ...
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const showRegisterLink = document.getElementById('show-register');
    const showLoginLink = document.getElementById('show-login');
    const authContainer = document.getElementById('auth-container');
    const appContainer = document.getElementById('app-container');
    const authMessage = document.getElementById('auth-message');
    const taskList = document.getElementById('task-list');
    const logoutButton = document.getElementById('logout-button');
    const addTaskForm = document.getElementById('add-task-form');

    const API_URL = 'http://127.0.0.1:8000';

    const token = localStorage.getItem('accessToken');
    if (token) {
        authContainer.classList.add('hidden');
        appContainer.classList.remove('hidden');
        fetchTasks();
    }
    
    showRegisterLink.addEventListener('click', (e) => {
        e.preventDefault();
        authMessage.textContent = '';
        loginForm.classList.add('hidden');
        registerForm.classList.remove('hidden');
    });

    showLoginLink.addEventListener('click', (e) => {
        e.preventDefault();
        authMessage.textContent = '';
        registerForm.classList.add('hidden');
        loginForm.classList.remove('hidden');
    });

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        authMessage.textContent = '';
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;
        
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);

        try {
            const response = await fetch(`${API_URL}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Falha no login');
            }

            const data = await response.json();
            localStorage.setItem('accessToken', data.access_token);
            authContainer.classList.add('hidden');
            appContainer.classList.remove('hidden');
            await fetchTasks();

        } catch (error) {
            authMessage.textContent = error.message;
        }
    });

    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        authMessage.textContent = '';
        const email = document.getElementById('register-email').value;
        const password = document.getElementById('register-password').value;

        try {
            const response = await fetch(`${API_URL}/usuarios/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: email, senha: password }),
            });

            if (response.status === 400) {
                throw new Error('Email já registado. Tente outro.');
            }
            if (!response.ok) {
                throw new Error('Ocorreu um erro ao registar.');
            }
            
            authMessage.style.color = 'green';
            authMessage.textContent = 'Usuário criado com sucesso! Por favor, faça o login.';
            
            registerForm.classList.add('hidden');
            loginForm.classList.remove('hidden');
            registerForm.reset();

        } catch (error) {
            authMessage.style.color = 'red';
            authMessage.textContent = error.message;
        }
    });

    logoutButton.addEventListener('click', () => {
        localStorage.removeItem('accessToken');
        authContainer.classList.remove('hidden');
        appContainer.classList.add('hidden');
        loginForm.reset();
        registerForm.reset();
        authMessage.textContent = '';
    });

    addTaskForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const title = document.getElementById('task-title').value;
        const description = document.getElementById('task-description').value;
        const token = localStorage.getItem('accessToken');

        try {
            const response = await fetch(`${API_URL}/tarefas/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    titulo: title,
                    descricao: description,
                    concluida: false
                })
            });

            if (!response.ok) {
                throw new Error('Não foi possível adicionar a tarefa.');
            }

            addTaskForm.reset();
            await fetchTasks();

        } catch (error) {
            document.getElementById('app-message').textContent = error.message;
        }
    });

    // LÓGICA DE CLIQUES NA LISTA DE TAREFAS (ATUALIZADA)
    taskList.addEventListener('click', async (e) => {
        const target = e.target;
        const taskItem = target.closest('.task-item');
        if (!taskItem) return;

        const taskId = taskItem.dataset.id;
        const token = localStorage.getItem('accessToken');
        const isCompleted = taskItem.classList.contains('completed');

        // Deletar tarefa
        if (target.classList.contains('delete-btn')) {
            try {
                await fetch(`${API_URL}/tarefas/${taskId}`, {
                    method: 'DELETE',
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                await fetchTasks();
            } catch (error) { console.error(error.message); }
        }

        // Concluir tarefa
        if (target.classList.contains('complete-btn')) {
            const currentTitle = taskItem.querySelector('.task-details strong').textContent;
            const currentDesc = taskItem.querySelector('.task-details p').textContent;
            try {
                await fetch(`${API_URL}/tarefas/${taskId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ titulo: currentTitle, descricao: currentDesc, concluida: true })
                });
                await fetchTasks();
            } catch (error) { console.error(error.message); }
        }

        // *** NOVO: Entrar no modo de edição ***
        if (target.classList.contains('edit-btn')) {
            const taskDetails = taskItem.querySelector('.task-details');
            const currentTitle = taskDetails.querySelector('strong').textContent;
            const currentDesc = taskDetails.querySelector('p').textContent;

            taskDetails.innerHTML = `
                <input type="text" class="edit-title" value="${currentTitle}">
                <input type="text" class="edit-desc" value="${currentDesc}">
            `;
            
            target.textContent = 'Salvar';
            target.classList.remove('edit-btn');
            target.classList.add('save-btn');
        }

        // *** NOVO: Salvar a edição ***
        else if (target.classList.contains('save-btn')) {
            const newTitle = taskItem.querySelector('.edit-title').value;
            const newDesc = taskItem.querySelector('.edit-desc').value;
            
            try {
                await fetch(`${API_URL}/tarefas/${taskId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        titulo: newTitle,
                        descricao: newDesc,
                        concluida: isCompleted // Mantém o status original
                    })
                });
                await fetchTasks();
            } catch (error) { console.error(error.message); }
        }
    });


    async function fetchTasks() {
        //... (função sem alterações)
        const token = localStorage.getItem('accessToken');
        if (!token) {
            logoutButton.click();
            return;
        }

        try {
            const response = await fetch(`${API_URL}/tarefas/`, {
                method: 'GET',
                headers: { 'Authorization': `Bearer ${token}` },
            });

            if (response.status === 401) {
                logoutButton.click();
                throw new Error('Sessão expirada. Faça login novamente.');
            }
            if (!response.ok) {
                throw new Error('Não foi possível carregar as tarefas.');
            }

            const tasks = await response.json();
            displayTasks(tasks);

        } catch (error) {
            authMessage.textContent = error.message;
        }
    }
    
    // FUNÇÃO DISPLAY ATUALIZADA COM O BOTÃO "EDITAR"
    function displayTasks(tasks) {
        taskList.innerHTML = '';
        
        if (tasks.length === 0) {
            taskList.innerHTML = '<li class="task-item">Nenhuma tarefa encontrada. Adicione uma!</li>';
            return;
        }

        tasks.forEach(task => {
            const li = document.createElement('li');
            li.className = 'task-item';
            if (task.concluida) {
                li.classList.add('completed');
            }
            li.dataset.id = task.id;

            li.innerHTML = `
                <div class="task-details">
                    <strong>${task.titulo}</strong>
                    <p>${task.descricao || ''}</p>
                </div>
                <div class="task-actions">
                    <span class="status">${task.concluida ? 'Concluída' : 'Pendente'}</span>
                    ${!task.concluida ? '<button class="complete-btn">Concluir</button>' : ''}
                    <button class="edit-btn">Editar</button>
                    <button class="delete-btn">Deletar</button>
                </div>
            `;
            taskList.appendChild(li);
        });
    }
});