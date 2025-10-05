/**
 * Garante que o código JavaScript só vai rodar
 * depois que toda a página HTML for carregada e estiver pronta.
 */
document.addEventListener('DOMContentLoaded', () => {
    
    // --- Seletores de Elementos ---
    // Guardamos em constantes os elementos do HTML que vamos manipular.

    // Elementos de autenticação (login/registro)
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const showRegisterLink = document.getElementById('show-register');
    const showLoginLink = document.getElementById('show-login');
    const authContainer = document.getElementById('auth-container');
    const authMessage = document.getElementById('auth-message');

    // Elementos principais da aplicação
    const appContainer = document.getElementById('tasks-page-container');
    const taskList = document.getElementById('task-list');
    const logoutButton = document.getElementById('logout-button');
    const addTaskForm = document.getElementById('add-task-form');

    // Elementos do seletor de tema
    const themeToggleButton = document.getElementById('theme-toggle-button');
    const themeIcon = themeToggleButton.querySelector('i');

    // Elementos do seletor de filtros e ordenação
    const filterButtonsContainer = document.querySelector('.filter-buttons');
    const sortSelect = document.getElementById('sort-select');

    // --- Configuração da API ---
    // URL base do nosso backend FastAPI
    const API_URL = 'https://web-production-889f.up.railway.app';


    // --- Gerenciamento do Tema (Modo Noturno) ---
    /**
     * Prepara e controla a troca de tema entre claro e escuro.
     * A preferência do usuário é salva no navegador para visitas futuras.
     */
    function setupTheme() {
        // Verifica se o usuário já tinha um tema salvo
        const currentTheme = localStorage.getItem('theme');
        if (currentTheme === 'dark') {
            document.body.classList.add('dark-mode');
            themeIcon.classList.replace('fa-moon', 'fa-sun');
        }

        // Adiciona o evento de clique ao botão de troca de tema
        themeToggleButton.addEventListener('click', () => {
            document.body.classList.toggle('dark-mode');
            
            let theme = 'light';
            // Verifica qual tema está ativo para salvar a escolha
            if (document.body.classList.contains('dark-mode')) {
                theme = 'dark';
                themeIcon.classList.replace('fa-moon', 'fa-sun'); // Troca ícone para sol
            } else {
                themeIcon.classList.replace('fa-sun', 'fa-moon'); // Troca ícone para lua
            }
            localStorage.setItem('theme', theme); // Salva a escolha
        });
    }


    let allTasks = []; // Guarda a lista original de tarefas vinda da API
    let currentFilter = 'all'; // 'all', 'pending', 'completed'
    let currentSort = 'priority'; // 'priority', 'dueDate'


    // --- Inicialização da Aplicação ---
    /**
     * Função principal que inicia o app.
     * Chama a função de tema e verifica se o usuário já está logado.
     */
    function initializeApp() {
        setupTheme(); // Configura o tema
        const token = localStorage.getItem('accessToken');
        if (token) {
            // Se encontrou um token, mostra o app principal
            authContainer.classList.add('hidden');
            appContainer.classList.remove('hidden');
            fetchTasks(); // Busca as tarefas do usuário
        }
        // Se não houver token, a tela de login/registro continua visível
    }

    // --- Eventos dos Formulários de Autenticação ---
    // Alterna entre os formulários de login e registro
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

    // Lida com o envio do formulário de login
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

    // Lida com o envio do formulário de registro
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

    // Lida com o clique no botão de logout
    logoutButton.addEventListener('click', () => {
        localStorage.removeItem('accessToken');
        authContainer.classList.remove('hidden');
        appContainer.classList.add('hidden');
        loginForm.reset();
        registerForm.reset();
        authMessage.textContent = '';
    });

    // --- Gerenciamento de Tarefas ---
    // Lida com o envio do formulário para adicionar nova tarefa
    addTaskForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const title = document.getElementById('task-title').value;
        const description = document.getElementById('task-description').value;
        const dueDate = document.getElementById('task-due-date').value;
        const priority = document.getElementById('task-priority').value;
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
                    concluida: false,
                    data_vencimento: dueDate || null, // Envia null se a data estiver vazia
                    prioridade: priority
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

    filterButtonsContainer.addEventListener('click', (e) => {
        if (e.target.classList.contains('filter-btn')) {
            // Remove a classe 'active' de todos os botões
            filterButtonsContainer.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
            // Adiciona a classe 'active' ao botão clicado
            e.target.classList.add('active');
            
            currentFilter = e.target.dataset.filter;
            renderTasks(); // Re-renderiza a lista com o novo filtro
        }
    });

    sortSelect.addEventListener('change', (e) => {
        currentSort = e.target.value;
        renderTasks(); // Re-renderiza a lista com a nova ordem
    });

    /**
     * Gerencia todos os cliques na lista de tarefas para
     * deletar, concluir ou editar uma tarefa.
     */
    taskList.addEventListener('click', async (e) => {
        const target = e.target;
        const taskItem = target.closest('.task-item');
        if (!taskItem) return;
    
        const taskId = taskItem.dataset.id;
        const token = localStorage.getItem('accessToken');
        const isCompleted = taskItem.classList.contains('completed'); // Pega o status atual
    
        // --- LÓGICA CENTRALIZADA PARA COMPLETAR E DESFAZER TAREFAS ---
        if (target.closest('.complete-btn, .uncomplete-btn')) {
            const newCompletedStatus = target.closest('.complete-btn') ? true : false;
    
            try {
                // 1. Busca os dados atuais e completos da tarefa
                const response = await fetch(`${API_URL}/tarefas/${taskId}`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                if (!response.ok) throw new Error('Não foi possível buscar os dados da tarefa para atualizar.');
                
                const taskData = await response.json();
    
                // 2. Envia o objeto COMPLETO de volta, alterando apenas o status 'concluida'
                await fetch(`${API_URL}/tarefas/${taskId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        ...taskData, 
                        concluida: newCompletedStatus 
                    })
                });
    
                await fetchTasks();
            } catch (error) { console.error(error.message); }
        }
        
        // --- LÓGICA DE DELETAR ---
        if (target.closest('.delete-btn')) {
            try {
                await fetch(`${API_URL}/tarefas/${taskId}`, {
                    method: 'DELETE',
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                await fetchTasks();
            } catch (error) { console.error(error.message); }
        }
    
        // --- LÓGICA DE EDIÇÃO ---
        // (O bloco duplicado de "Concluir" foi removido daqui)
        if (target.closest('.edit-btn')) {
            const taskDetails = taskItem.querySelector('.task-details');
            const currentTitle = taskDetails.querySelector('strong').textContent;
            const currentDesc = taskDetails.querySelector('p').textContent;
    
            taskDetails.innerHTML = `
                <input type="text" class="edit-title" value="${currentTitle}">
                <input type="text" class="edit-desc" value="${currentDesc}">
            `;
            
            const editButton = taskItem.querySelector('.edit-btn');
            editButton.innerHTML = '<i class="fas fa-save"></i>';
            editButton.title = 'Salvar';
            editButton.classList.replace('edit-btn', 'save-btn');
        }
        else if (target.closest('.save-btn')) {
            const newTitle = taskItem.querySelector('.edit-title').value;
            const newDesc = taskItem.querySelector('.edit-desc').value;
            
            try {
                // ATENÇÃO: A lógica de salvar também precisa ser atualizada no futuro
                // para preservar a data e a prioridade, assim como fizemos com o botão de concluir.
                const response = await fetch(`${API_URL}/tarefas/${taskId}`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                const taskData = await response.json();
    
                await fetch(`${API_URL}/tarefas/${taskId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        ...taskData,
                        titulo: newTitle,
                        descricao: newDesc,
                    })
                });
                await fetchTasks();
            } catch (error) { console.error(error.message); }
        }
    });


    // --- Funções de Requisição à API ---
    /**
     * Busca as tarefas do usuário na API e chama a função para exibi-las.
     */
    async function fetchTasks() {
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

            allTasks = await response.json(); // Salva a lista original na variável global
            renderTasks(); // Chama a nova função de renderização

        } catch (error) {
            authMessage.textContent = error.message;
        }
    }
    
    /**
     * Exibe as tarefas na tela, criando os elementos HTML para cada uma.
     * @param {Array} tasks - Uma lista de objetos de tarefa vindos da API.
     */
    function renderTasks() {
        let tasksToRender = [...allTasks];

        // 1. APLICA O FILTRO ATUAL
        if (currentFilter === 'pending') {
            tasksToRender = tasksToRender.filter(task => !task.concluida);
        } else if (currentFilter === 'completed') {
            tasksToRender = tasksToRender.filter(task => task.concluida);
        }

        // 2. APLICA A ORDENAÇÃO ATUAL
        if (currentSort === 'priority') {
            const priorityOrder = { 'vermelha': 1, 'amarela': 2, 'verde': 3 };
            tasksToRender.sort((a, b) => {
                const priorityA = priorityOrder[a.prioridade] || 99;
                const priorityB = priorityOrder[b.prioridade] || 99;
                if (priorityA !== priorityB) {
                    return priorityA - priorityB;
                }
                // Critério de desempate: data
                const dateA = a.data_vencimento ? new Date(a.data_vencimento) : null;
                const dateB = b.data_vencimento ? new Date(b.data_vencimento) : null;
                if (!dateA) return 1;
                if (!dateB) return -1;
                return dateA - dateB;
            });
        } else if (currentSort === 'dueDate') {
            tasksToRender.sort((a, b) => {
                const dateA = a.data_vencimento ? new Date(a.data_vencimento) : null;
                const dateB = b.data_vencimento ? new Date(b.data_vencimento) : null;
                if (!dateA) return 1; // Tarefas sem data vão para o final
                if (!dateB) return -1;
                return dateA - dateB;
            });
        }

        // 3. RENDERIZA O RESULTADO NA TELA
        taskList.innerHTML = '';
        if (tasksToRender.length === 0) {
            taskList.innerHTML = '<li class="task-item" style="justify-content: center;">Nenhuma tarefa encontrada para este filtro.</li>';
            return;
        }

        tasksToRender.forEach(task => {
            const li = document.createElement('li');
            li.className = 'task-item';
            li.classList.add(`priority-${task.prioridade}`);
            if (task.concluida) {
                li.classList.add('completed');
            }
            li.dataset.id = task.id;

            let dueDate = '';
            if (task.data_vencimento) {
                const date = new Date(task.data_vencimento + 'T00:00:00');
                dueDate = `<span class="due-date"><i class="fas fa-calendar-alt"></i> ${date.toLocaleDateString('pt-BR')}</span>`;
            }

            const completeButton = task.concluida
                ? `<button class="uncomplete-btn" title="Desfazer"><i class="fas fa-undo"></i></button>`
                : `<button class="complete-btn" title="Concluir"><i class="fas fa-check"></i></button>`;

            li.innerHTML = `
                <div class="task-info">
                    <div class="task-details">
                        <strong>${task.titulo}</strong>
                        <p>${task.descricao || ''}</p>
                    </div>
                    ${dueDate}
                </div>
                <div class="task-actions">
                    ${completeButton}
                    <button class="edit-btn" title="Editar"><i class="fas fa-pencil-alt"></i></button>
                    <button class="delete-btn" title="Deletar"><i class="fas fa-trash"></i></button>
                </div>
            `;
            taskList.appendChild(li);
        });
    }

    // Inicia a aplicação quando a página é carregada
    initializeApp();
});