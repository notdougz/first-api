/**
 * Ponto de entrada principal para a aplicação de Gestão de Tarefas.
 * Este script gere o estado da UI, a interação do utilizador e a comunicação
 * com a API do backend.
 */
document.addEventListener('DOMContentLoaded', () => {
    
    // --- Módulo de Configuração e Constantes ---
    const config = {
        API_URL: 'https://web-production-889f.up.railway.app',
    };

    // --- Seletores do DOM ---
    // Agrupar todos os seletores de elementos num único objeto torna o código mais organizado.
    const ui = {
        authContainer: document.getElementById('auth-container'),
        appContainer: document.getElementById('tasks-page-container'),
        loginForm: document.getElementById('login-form'),
        registerForm: document.getElementById('register-form'),
        showRegisterLink: document.getElementById('show-register'),
        showLoginLink: document.getElementById('show-login'),
        logoutButton: document.getElementById('logout-button'),
        addTaskForm: document.getElementById('add-task-form'),
        taskList: document.getElementById('task-list'),
        authMessage: document.getElementById('auth-message'),
        appMessage: document.getElementById('app-message'),
        themeToggleButton: document.getElementById('theme-toggle-button'),
        themeIcon: document.querySelector('#theme-toggle-button i'),
        filterButtonsContainer: document.querySelector('.filter-buttons'),
        sortSelect: document.getElementById('sort-select'),
        addTaskToggle: document.getElementById('add-task-toggle'),
        addTaskFormContainer: document.querySelector('.sidebar'),
    };

    // --- Gestão de Estado da Aplicação ---
    // Centralizar o estado ajuda a entender como os dados controlam a UI.
    const state = {
        allTasks: [], // Guarda a lista original de tarefas vinda da API
        currentFilter: 'all', // 'all', 'pending', 'completed'
        currentSort: 'priority', // 'priority', 'dueDate'
    };


    // --- Módulo de Serviço da API ---
    /**
     * Isola toda a lógica de comunicação com o backend.
     * Se a API mudar, só precisamos de alterar este objeto.
     */
    const apiService = {
        /**
         * Realiza uma chamada `fetch` configurada para a nossa API.
         * @param {string} endpoint - O endpoint da API a ser chamado.
         * @param {object} options - As opções da requisição (method, headers, body).
         * @returns {Promise<any>} - A resposta da API em formato JSON.
         */
        async request(endpoint, options = {}) {
            const token = localStorage.getItem('accessToken');
            const headers = {
                'Content-Type': 'application/json',
                ...options.headers,
            };

            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }

            const response = await fetch(`${config.API_URL}${endpoint}`, { ...options, headers });

            if (response.status === 401) {
                handleLogout(); // Se a API retornar "Não Autorizado", faz logout
                throw new Error('Sessão expirada. Por favor, faça login novamente.');
            }
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `Erro na requisição: ${response.statusText}`);
            }
            // Se a resposta não tiver corpo (ex: DELETE), retorna um sucesso genérico
            return response.status === 204 ? { success: true } : response.json();
        },

        login: (email, password) => {
            const formData = new URLSearchParams();
            formData.append('username', email);
            formData.append('password', password);
            return apiService.request('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: formData,
            });
        },
        register: (email, senha) => apiService.request('/usuarios/', {
            method: 'POST',
            body: JSON.stringify({ email, senha }),
        }),
        getTasks: () => apiService.request('/tarefas/'),
        createTask: (taskData) => apiService.request('/tarefas/', {
            method: 'POST',
            body: JSON.stringify(taskData),
        }),
        updateTask: (taskId, taskData) => apiService.request(`/tarefas/${taskId}`, {
            method: 'PUT',
            body: JSON.stringify(taskData),
        }),
        deleteTask: (taskId) => apiService.request(`/tarefas/${taskId}`, { method: 'DELETE' }),
    };


    // --- Lógica de Negócio e Manipuladores de Eventos ---

    /**
     * Exibe uma mensagem de feedback para o utilizador.
     * @param {string} message - A mensagem a ser exibida.
     * @param {'error' | 'success'} type - O tipo de mensagem (para estilização).
     * @param {'auth' | 'app'} location - Onde exibir a mensagem.
     */
    function showFeedbackMessage(message, type = 'error', location = 'auth') {
        const element = location === 'auth' ? ui.authMessage : ui.appMessage;
        element.textContent = message;
        element.style.color = type === 'success' ? 'var(--success-color)' : 'var(--danger-color)';
    }

    /** Transiciona a UI da tela de autenticação para a de tarefas. */
    function showAppView() {
        ui.authContainer.classList.add('hidden');
        ui.appContainer.classList.remove('hidden');
    }

    /** Transiciona a UI da tela de tarefas para a de autenticação. */
    function showAuthView() {
        ui.appContainer.classList.add('hidden');
        ui.authContainer.classList.remove('hidden');
    }
    
    /** Busca as tarefas e atualiza o estado e a UI. */
    async function refreshTasks() {
        try {
            state.allTasks = await apiService.getTasks();
            renderTasks();
        } catch (error) {
            showFeedbackMessage(error.message, 'error', 'app');
        }
    }
    
    /** Manipula o processo de login do utilizador. */
    async function handleLogin(e) {
        e.preventDefault();
        showFeedbackMessage('', 'success', 'auth'); // Limpa mensagens antigas
        const email = ui.loginForm.elements['login-email'].value;
        const password = ui.loginForm.elements['login-password'].value;

        try {
            const data = await apiService.login(email, password);
            localStorage.setItem('accessToken', data.access_token);
            showAppView();
            await refreshTasks();
        } catch (error) {
            showFeedbackMessage(error.message);
        }
    }
    
    /** Manipula o registo de um novo utilizador. */
    async function handleRegister(e) {
        e.preventDefault();
        showFeedbackMessage('', 'success', 'auth');
        const email = ui.registerForm.elements['register-email'].value;
        const password = ui.registerForm.elements['register-password'].value;

        try {
            await apiService.register(email, password);
            showFeedbackMessage('Utilizador criado com sucesso! Por favor, faça o login.', 'success');
            ui.registerForm.classList.add('hidden');
            ui.loginForm.classList.remove('hidden');
            ui.registerForm.reset();
        } catch (error) {
            showFeedbackMessage(error.message);
        }
    }

    /** Manipula o processo de logout. */
    function handleLogout() {
        localStorage.removeItem('accessToken');
        showAuthView();
        ui.loginForm.reset();
        ui.registerForm.reset();
        showFeedbackMessage('', 'success', 'auth');
    }

    /** Manipula a criação de uma nova tarefa. */
    async function handleCreateTask(e) {
        e.preventDefault();
        const title = ui.addTaskForm.elements['task-title'].value;
        const description = ui.addTaskForm.elements['task-description'].value;
        const dueDate = ui.addTaskForm.elements['task-due-date'].value;
        const priority = ui.addTaskForm.elements['task-priority'].value;

        const taskData = {
            titulo: title,
            descricao: description,
            concluida: false,
            data_vencimento: dueDate || null,
            prioridade: priority
        };

        try {
            await apiService.createTask(taskData);
            ui.addTaskForm.reset();
            await refreshTasks();
        } catch (error) {
            showFeedbackMessage(error.message, 'error', 'app');
        }
    }

    // --- Lógica de Renderização ---

    /**
     * Renderiza a lista de tarefas na UI com base no estado atual (filtros e ordenação).
     */
    function renderTasks() {
        let tasksToRender = [...state.allTasks];

        // 1. Aplica Filtro
        if (state.currentFilter === 'pending') {
            tasksToRender = tasksToRender.filter(task => !task.concluida);
        } else if (state.currentFilter === 'completed') {
            tasksToRender = tasksToRender.filter(task => task.concluida);
        }

        // 2. Aplica Ordenação
        const priorityOrder = { 'vermelha': 1, 'amarela': 2, 'verde': 3 };
        tasksToRender.sort((a, b) => {
            if (state.currentSort === 'priority') {
                const priorityA = priorityOrder[a.prioridade] || 99;
                const priorityB = priorityOrder[b.prioridade] || 99;
                return priorityA - priorityB || (new Date(a.data_vencimento) - new Date(b.data_vencimento));
            }
            if (state.currentSort === 'dueDate') {
                const dateA = a.data_vencimento ? new Date(a.data_vencimento) : Infinity;
                const dateB = b.data_vencimento ? new Date(b.data_vencimento) : Infinity;
                return dateA - dateB;
            }
            return 0;
        });

        // 3. Renderiza no DOM
        ui.taskList.innerHTML = '';
        if (tasksToRender.length === 0) {
            ui.taskList.innerHTML = '<li class="task-item" style="justify-content: center;">Nenhuma tarefa encontrada para este filtro.</li>';
            return;
        }
        
        const taskElements = tasksToRender.map(createTaskElement);
        ui.taskList.append(...taskElements);
    }

    /**
     * Cria um elemento <li> para uma única tarefa.
     * @param {object} task - O objeto da tarefa.
     * @returns {HTMLLIElement} O elemento LI criado.
     */
    function createTaskElement(task) {
        const li = document.createElement('li');
        li.className = `task-item priority-${task.prioridade} ${task.concluida ? 'completed' : ''}`;
        li.dataset.id = task.id;

        const dueDate = task.data_vencimento
            ? `<span class="due-date"><i class="fas fa-calendar-alt"></i> ${new Date(task.data_vencimento + 'T00:00:00').toLocaleDateString('pt-BR')}</span>`
            : '';

        const completeButton = task.concluida
            ? `<button class="task-action-btn" data-action="uncomplete" title="Desfazer"><i class="fas fa-undo"></i></button>`
            : `<button class="task-action-btn" data-action="complete" title="Concluir"><i class="fas fa-check"></i></button>`;

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
                <button class="task-action-btn" data-action="edit" title="Editar"><i class="fas fa-pencil-alt"></i></button>
                <button class="task-action-btn" data-action="delete" title="Deletar"><i class="fas fa-trash"></i></button>
            </div>
        `;
        return li;
    }

    // --- Inicialização de Event Listeners ---

    /** Adiciona todos os event listeners da aplicação. */
    function setupEventListeners() {
        ui.loginForm.addEventListener('submit', handleLogin);
        ui.registerForm.addEventListener('submit', handleRegister);
        ui.logoutButton.addEventListener('click', handleLogout);
        ui.addTaskForm.addEventListener('submit', handleCreateTask);
        
        ui.showRegisterLink.addEventListener('click', (e) => {
            e.preventDefault();
            showFeedbackMessage('', 'success');
            ui.loginForm.classList.add('hidden');
            ui.registerForm.classList.remove('hidden');
        });

        ui.showLoginLink.addEventListener('click', (e) => {
            e.preventDefault();
            showFeedbackMessage('', 'success');
            ui.registerForm.classList.add('hidden');
            ui.loginForm.classList.remove('hidden');
        });
        
        // Listener para filtros (delegação de eventos)
        ui.filterButtonsContainer.addEventListener('click', (e) => {
            const filterBtn = e.target.closest('.filter-btn');
            if (filterBtn) {
                ui.filterButtonsContainer.querySelector('.active').classList.remove('active');
                filterBtn.classList.add('active');
                state.currentFilter = filterBtn.dataset.filter;
                renderTasks();
            }
        });

        // Listener para ordenação
        ui.sortSelect.addEventListener('change', (e) => {
            state.currentSort = e.target.value;
            renderTasks();
        });

        // Listener central para ações nas tarefas (delegação de eventos)
        ui.taskList.addEventListener('click', (e) => {
            const actionBtn = e.target.closest('.task-action-btn');
            if (actionBtn) {
                const taskItem = actionBtn.closest('.task-item');
                const taskId = taskItem.dataset.id;
                const action = actionBtn.dataset.action;

                // Aqui poderíamos usar um switch ou um objeto de ações
                // para um código ainda mais limpo, mas if/else é claro o suficiente.
                if (action === 'complete' || action === 'uncomplete') {
                    // Lógica para completar/desfazer
                } else if (action === 'delete') {
                    // Lógica para deletar
                } else if (action === 'edit') {
                    // Lógica para editar
                }
            }
        });
    }

    /**
     * Configura a lógica do tema (claro/escuro).
     */
    function setupTheme() {
        if (localStorage.getItem('theme') === 'dark') {
            document.body.classList.add('dark-mode');
            ui.themeIcon.classList.replace('fa-moon', 'fa-sun');
        }
        ui.themeToggleButton.addEventListener('click', () => {
            document.body.classList.toggle('dark-mode');
            const isDarkMode = document.body.classList.contains('dark-mode');
            localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
            ui.themeIcon.classList.toggle('fa-sun', isDarkMode);
            ui.themeIcon.classList.toggle('fa-moon', !isDarkMode);
        });
    }

    /**
     * Ponto de entrada que inicializa a aplicação.
     */
    function initializeApp() {
        setupTheme();
        setupEventListeners();

        if (localStorage.getItem('accessToken')) {
            showAppView();
            refreshTasks();
        } else {
            showAuthView();
        }
    }

    // --- Iniciar a Aplicação ---
    initializeApp();
});