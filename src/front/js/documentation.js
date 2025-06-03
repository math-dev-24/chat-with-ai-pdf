    const {createApp, reactive, onMounted} = Vue;

    const goLoadPdf = async () => {
        const res = await fetch('/pdfs/process-all', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "Accept": "application/json",
            }
        });
        if (!res.ok){
            throw new Error(res.statusText);
        }
        return await res.json()
    }

    const clearCollection = async () => {
        const res = await fetch('/collection/clear', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                "Accept": "application/json",
            }
        })
        if (!res.ok){
            throw new Error(res.statusText);
        }
        return await res.json()
    }

    createApp({
        setup() {
            const vectorState = reactive({
                errors: [],
                error_count: 0,
                processed_count: 0,
                processed_files: [],
                inLoading: false,
            })

            const statState = reactive({
                total_chunks: 0,
                total_files: 0,
                files: [],
            })

            const getStats = async () => {
                const res = await fetch("/stat")

                if (res.status === 200) {
                    const data = await res.json()
                    console.log(data)
                    statState.total_chunks = data.total_chunks;
                    statState.total_files = data.total_files;
                    statState.files = data.files
                }
            }

            const handleLoadPdf = async () => {
                vectorState.errors = [];
                vectorState.error_count = 0;
                vectorState.processed_count = 0;
                vectorState.processed_files = [];
                vectorState.inLoading = true;

                try {
                    const res = await goLoadPdf();
                    vectorState.errors = res.errors || [];
                    vectorState.error_count = res.error_count || 0;
                    vectorState.processed_count = res.processed_count || 0;
                    vectorState.processed_files = res.processed_files || [];
                    await getStats();
                } catch (error) {
                    console.error(error);
                    vectorState.errors = [`Erreur de communication: ${error.message}`];
                    vectorState.error_count = 1;
                } finally {
                    vectorState.inLoading = false;
                }
            }

            const handleClear = async () => {
                vectorState.inLoading = true;
                try {
                    await clearCollection()
                    await getStats();
                } catch (error) {
                    console.error(error);
                } finally {
                    vectorState.inLoading = false;
                }
            }

            onMounted( async () => {
                await getStats();
            })

            return {
                handleLoadPdf,
                handleClear,
                vectorState,
                statState
            };
        }
    }).mount('#app');