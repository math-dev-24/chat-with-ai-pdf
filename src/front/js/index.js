    const {createApp, reactive, computed} = Vue;

    const response = async (question) => {
        try {
            const res = await fetch('/ask', {
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    method: 'POST',
                    body: JSON.stringify({question: question})
                }
            )
            return await res.json()
        } catch (error) {
            throw error
        }
    }

    createApp({
        setup() {
            const state = reactive({
                answer: "",
                inLoading: false,
                context: [],
                dialog: [{
                    id: 1,
                    role: "system",
                    message: `Bonjour ! Comment puis-je vous aider aujourd'hui ?`
                }],
                error: '',
                showContext: false
            });

            const isDisabled = computed(() => state.answer.trim() === "" || state.inLoading);

            const handleSubmit = async () => {
                state.error = '';
                state.inLoading = true;

                if (state.answer.trim() === '') {
                    state.error = 'Veuillez saisir une question';
                    state.inLoading = false;
                    return;
                }

                state.dialog.push({
                    id: Date.now(),
                    role: "user",
                    message: state.answer,
                })

                const currentQuestion = state.answer;
                state.answer = "";

                try {
                    const res = await response(currentQuestion);

                    state.dialog.push({
                        id: Date.now() + 1,
                        role: "system",
                        message: res.response
                    })

                    state.context.push(res.context)

                } catch (error) {
                    state.error = "Erreur lors de la communication avec le serveur";
                    console.error(`Erreur : ${error}`)
                } finally {
                    state.inLoading = false;
                }
            }

            const toggleContextPanel = () => {
                state.showContext = !state.showContext;
            }

            return {
                handleSubmit,
                toggleContextPanel,
                isDisabled,
                state
            };
        }
    }).mount('#app');