<script lang="ts">
	import { base_url_api } from '$lib/const';

	import { Card, CardContent, CardHeader, CardTitle } from "$lib/components/ui/card";
	import { Button } from "$lib/components/ui/button";
	import { Alert, AlertDescription } from "$lib/components/ui/alert";
	import { ScrollArea } from "$lib/components/ui/scroll-area";

	import {
		FileText,
		Folder,
		Database,
		Zap,
		CheckCircle,
		AlertCircle,
		Loader2,
		FolderOpen,
		Trash2
	} from "lucide-svelte";

	let { data } = $props();

	let inLoading = $state<boolean>(false);
	let error = $state<string | null>(null);
	let success = $state<boolean>(false);
	let deletingFile = $state<string | null>(null);

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

	const handleDeleteFile = async (fileName: string) => {
		if (!confirm('Êtes-vous sûr de vouloir supprimer ce fichier ?')) {
			return;
		}

		try {
			deletingFile = fileName;
			const response = await fetch(`/api/files/${fileName}`, {
				method: 'DELETE'
			});

			if (!response.ok) {
				throw new Error(`Erreur HTTP: ${response.status}`);
			}

			data.stat.files = data.stat.files.filter((file: string) => file !== fileName);
			data.stat.total_files--;
			success = true;
			setTimeout(() => success = false, 3000);
		} catch (err) {
			error = err instanceof Error ? err.message : 'Une erreur est survenue';
			console.error('Erreur lors de la suppression du fichier:', err);
		} finally {
			deletingFile = null;
		}
	};
</script>

<div class="max-w-4xl mx-auto p-6 space-y-6">
	<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
		<Card class="hover:shadow-md transition-shadow">
			<CardContent class="flex items-center p-6">
				<div class="flex items-center justify-center w-12 h-12 bg-primary/10 rounded-lg mr-4">
					<Database class="h-6 w-6 text-primary" />
				</div>
				<div class="flex-1">
					<p class="text-sm font-medium text-muted-foreground uppercase tracking-wide">
						Chunks
					</p>
					<p class="text-2xl font-bold text-foreground">
						{data.stat.total_chunks.toLocaleString()}
					</p>
				</div>
			</CardContent>
		</Card>

		<Card class="hover:shadow-md transition-shadow">
			<CardContent class="flex items-center p-6">
				<div class="flex items-center justify-center w-12 h-12 bg-secondary/10 rounded-lg mr-4">
					<FileText class="h-6 w-6 text-secondary-foreground" />
				</div>
				<div class="flex-1">
					<p class="text-sm font-medium text-muted-foreground uppercase tracking-wide">
						Fichiers
					</p>
					<p class="text-2xl font-bold text-foreground">
						{data.stat.total_files}
					</p>
				</div>
			</CardContent>
		</Card>
	</div>

	<Card>
		<CardHeader>
			<CardTitle class="flex items-center gap-2">
				<Folder class="h-5 w-5" />
				Liste des fichiers
			</CardTitle>
		</CardHeader>
		<CardContent>
			{#if data.stat.files.length > 0}
				<ScrollArea class="h-[300px] w-full">
					<div class="space-y-2 pr-4">
						{#each data.stat.files as file (file)}
							<div class="flex items-center gap-3 p-3 rounded-lg border bg-card hover:bg-muted/50 transition-colors">
								<FileText class="h-4 w-4 text-muted-foreground flex-shrink-0" />
								<span class="text-sm text-foreground truncate flex-1" title={file}>
									{file}
								</span>
								<Button
									variant="ghost"
									size="icon"
									class="h-8 w-8 text-destructive hover:text-destructive hover:bg-destructive/10"
									on:click={() => handleDeleteFile(file)}
									disabled={deletingFile === file}
								>
									{#if deletingFile === file}
										<Loader2 class="h-4 w-4 animate-spin" />
									{:else}
										<Trash2 class="h-4 w-4" />
									{/if}
								</Button>
							</div>
						{/each}
					</div>
				</ScrollArea>
			{:else}
				<div class="flex flex-col items-center justify-center py-12 text-center">
					<FolderOpen class="h-12 w-12 text-muted-foreground/60 mb-4" />
					<p class="text-muted-foreground">Aucun fichier trouvé</p>
				</div>
			{/if}
		</CardContent>
	</Card>

	{#if error}
		<Alert variant="destructive">
			<AlertCircle class="h-4 w-4" />
			<AlertDescription>{error}</AlertDescription>
		</Alert>
	{/if}

	{#if success}
		<Alert class="border-green-200 bg-green-50 text-green-800 dark:border-green-800 dark:bg-green-950 dark:text-green-200">
			<CheckCircle class="h-4 w-4" />
			<AlertDescription>
				Opération terminée avec succès !
			</AlertDescription>
		</Alert>
	{/if}

	<div class="flex justify-center pt-4">
		<Button
			onclick={handlePdfLoad}
			disabled={inLoading}
			size="lg"
			class="min-w-[200px] gap-2"
		>
			{#if inLoading}
				<Loader2 class="h-4 w-4 animate-spin" />
				Traitement en cours...
			{:else}
				<Zap class="h-4 w-4" />
				Traiter les PDFs
			{/if}
		</Button>
	</div>
</div>