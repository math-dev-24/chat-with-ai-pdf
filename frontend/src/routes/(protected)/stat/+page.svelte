<script lang="ts">
	import { base_url_api } from '$lib/const';

	let { data } = $props();

	let inLoading = $state<boolean>(false);
	let error = $state<string | null>(null);
	let success = $state<boolean>(false);

	const handlePdfLoad = async () => {
		try {
			inLoading = true;
			error = null;
			success = false;

			const response = await fetch(`${base_url_api}/pdfs/process-all`, {
				method: 'POST'
			});

			if (!response.ok) {
				throw new Error(`Erreur HTTP: ${response.status}`);
			}

			success = true;
			setTimeout(() => success = false, 3000);
		} catch (err) {
			error = err instanceof Error ? err.message : 'Une erreur est survenue';
			console.error('Erreur lors du traitement des PDFs:', err);
		} finally {
			inLoading = false;
		}
	};
</script>

<div class="pdf-dashboard">
	<!-- En-tête avec statistiques -->
	<div class="stats-container">
		<div class="stat-card">
			<div class="stat-icon">📊</div>
			<div class="stat-content">
				<p class="stat-label">Chunks</p>
				<p class="stat-value">{data.stat.total_chunks.toLocaleString()}</p>
			</div>
		</div>

		<div class="stat-card">
			<div class="stat-icon">📄</div>
			<div class="stat-content">
				<p class="stat-label">Fichiers</p>
				<p class="stat-value">{data.stat.total_files}</p>
			</div>
		</div>
	</div>

	<!-- Section des fichiers -->
	<div class="files-section">
		<h3 class="section-title">
			<span class="title-icon">📁</span>
			Liste des fichiers
		</h3>

		{#if data.stat.files.length > 0}
			<div class="files-grid">
				{#each data.stat.files as file (file)}
					<div class="file-item">
						<div class="file-icon">📄</div>
						<span class="file-name" title={file}>{file}</span>
					</div>
				{/each}
			</div>
		{:else}
			<div class="empty-state">
				<div class="empty-icon">📭</div>
				<p>Aucun fichier trouvé</p>
			</div>
		{/if}
	</div>

	<!-- Messages de statut -->
	{#if error}
		<div class="alert alert-error">
			<span class="alert-icon">❌</span>
			<span>{error}</span>
		</div>
	{/if}

	{#if success}
		<div class="alert alert-success">
			<span class="alert-icon">✅</span>
			<span>Traitement des PDFs terminé avec succès !</span>
		</div>
	{/if}

	<!-- Bouton d'action -->
	<div class="action-section">
		<button
			class="process-button"
			class:loading={inLoading}
			onclick={handlePdfLoad}
			disabled={inLoading}
		>
			{#if inLoading}
				<span class="spinner"></span>
				<span>Traitement en cours...</span>
			{:else}
				<span class="button-icon">⚡</span>
				<span>Traiter les PDFs</span>
			{/if}
		</button>
	</div>
</div>

<style>
    .pdf-dashboard {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background: #f8fafc;
        min-height: 100vh;
    }

    /* Statistiques */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }

    .stat-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        display: flex;
        align-items: center;
        gap: 1rem;
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
    }

    .stat-icon {
        font-size: 2rem;
        opacity: 0.8;
    }

    .stat-content {
        flex: 1;
    }

    .stat-label {
        margin: 0;
        font-size: 0.875rem;
        color: #64748b;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .stat-value {
        margin: 0.25rem 0 0 0;
        font-size: 1.875rem;
        font-weight: 700;
        color: #1e293b;
        line-height: 1;
    }

    /* Section des fichiers */
    .files-section {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
    }

    .section-title {
        margin: 0 0 1.5rem 0;
        font-size: 1.25rem;
        font-weight: 600;
        color: #1e293b;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .title-icon {
        font-size: 1.5rem;
    }

    .files-grid {
        display: grid;
        gap: 0.75rem;
        max-height: 300px;
        overflow-y: auto;
        padding-right: 0.5rem;
    }

    .files-grid::-webkit-scrollbar {
        width: 6px;
    }

    .files-grid::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 3px;
    }

    .files-grid::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 3px;
    }

    .file-item {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 0.75rem;
        background: #f8fafc;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        transition: background-color 0.2s, border-color 0.2s;
    }

    .file-item:hover {
        background: #f1f5f9;
        border-color: #cbd5e1;
    }

    .file-icon {
        font-size: 1.25rem;
        opacity: 0.7;
    }

    .file-name {
        flex: 1;
        font-size: 0.875rem;
        color: #475569;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .empty-state {
        text-align: center;
        padding: 3rem 1rem;
        color: #64748b;
    }

    .empty-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        opacity: 0.6;
    }

    /* Alertes */
    .alert {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        font-size: 0.875rem;
        font-weight: 500;
        animation: slideIn 0.3s ease-out;
    }

    .alert-error {
        background: #fef2f2;
        color: #dc2626;
        border: 1px solid #fecaca;
    }

    .alert-success {
        background: #f0fdff;
        color: #059669;
        border: 1px solid #a7f3d0;
    }

    .alert-icon {
        font-size: 1.125rem;
    }

    /* Section d'action */
    .action-section {
        display: flex;
        justify-content: center;
        padding-top: 1rem;
    }

    .process-button {
        background: linear-gradient(135deg, #3b82f6, #1e40af);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 1rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        transition: all 0.2s;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        min-width: 200px;
        justify-content: center;
    }

    .process-button:hover:not(:disabled) {
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
    }

    .process-button:active:not(:disabled) {
        transform: translateY(0);
    }

    .process-button:disabled {
        opacity: 0.7;
        cursor: not-allowed;
        transform: none;
    }

    .process-button.loading {
        background: linear-gradient(135deg, #6b7280, #4b5563);
    }

    .button-icon {
        font-size: 1.125rem;
    }

    .spinner {
        width: 1.125rem;
        height: 1.125rem;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-top: 2px solid white;
        border-radius: 50%;
        animation: spin 1s linear infinite;
		}
</style>