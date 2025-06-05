<script lang="ts">
	import { page } from "$app/state";

	// Composants shadcn-svelte
	import { Button } from "$lib/components/ui/button";
	import { Textarea } from "$lib/components/ui/textarea";
	import { Alert, AlertDescription } from "$lib/components/ui/alert";
	import { Badge } from "$lib/components/ui/badge";

	// Icônes Lucide
	import { Send, Loader2, Eye, EyeOff, AlertCircle, Paperclip } from "lucide-svelte";
	import { cn } from "$lib/utils";

	interface Props {
		answer: string;
		inLoading: boolean;
		error?: string;
		showContext?: boolean;
		onToggleContext?: () => void;
	}

	let {
		answer,
		inLoading,
		error = '',
		showContext = false,
		onToggleContext
	}: Props = $props();

	let isDisabled = $derived(!answer.trim() || inLoading);
	let textareaElement: HTMLTextAreaElement;

	// Auto-resize du textarea
	function handleInput() {
		if (textareaElement) {
			textareaElement.style.height = 'auto';
			textareaElement.style.height = Math.min(textareaElement.scrollHeight, 120) + 'px';
		}
	}

	// Soumission avec Ctrl+Enter
	function handleKeydown(e: KeyboardEvent) {
		if (e.key === 'Enter' && (e.ctrlKey || e.metaKey) && !isDisabled) {
			e.preventDefault();
			const form = textareaElement.closest('form');
			if (form) {
				const submitEvent = new Event('submit', { bubbles: true, cancelable: true });
				form.dispatchEvent(submitEvent);
			}
		}
	}
</script>

<!-- Input optimisé pour être collé au chat -->
<div class="bg-background border border-border rounded-lg shadow-sm">
	<!-- Message d'erreur en haut si présent -->
	{#if error}
		<div class="p-3 border-b">
			<Alert variant="destructive" class="py-2">
				<AlertCircle class="h-4 w-4" />
				<AlertDescription class="text-sm">
					{error}
				</AlertDescription>
			</Alert>
		</div>
	{/if}

	<form
		method="POST"
		action={`/chat/${page.params.id}?/postMessage`}
		class="p-4"
	>
		<!-- Zone de saisie -->
		<div class="space-y-3">
			<div class="relative">
        <Textarea
					bind:value={answer}
					bind:this={textareaElement}
					name="answer"
					placeholder="Tapez votre message... (Ctrl+Entrée pour envoyer)"
					class="resize-none min-h-[44px] max-h-[120px] pr-12 bg-muted/30 border-border/50 focus:bg-background"
					disabled={inLoading}
					oninput={handleInput}
					onkeydown={handleKeydown}
				/>

				<!-- Bouton attachement (optionnel) -->
				<Button
					type="button"
					variant="ghost"
					size="sm"
					class="absolute right-2 top-2 h-8 w-8 p-0 text-muted-foreground hover:text-foreground"
					disabled={inLoading}
				>
					<Paperclip class="h-4 w-4" />
				</Button>
			</div>

			<!-- Barre d'actions -->
			<div class="flex items-center justify-between">
				<!-- Contrôles gauche -->
				<div class="flex items-center gap-2">
					<!-- Bouton contexte -->
					{#if onToggleContext}
						<Button
							type="button"
							variant="outline"
							size="sm"
							onclick={onToggleContext}
							class="gap-2 text-xs"
							disabled={inLoading}
						>
							{#if showContext}
								<EyeOff class="h-3 w-3" />
								Masquer
							{:else}
								<Eye class="h-3 w-3" />
								Contexte
							{/if}
						</Button>
					{/if}

					<!-- Badge de statut -->
					{#if inLoading}
						<Badge variant="secondary" class="gap-1 text-xs">
							<Loader2 class="h-3 w-3 animate-spin" />
							Traitement...
						</Badge>
					{/if}
				</div>

				<!-- Bouton d'envoi -->
				<Button
					type="submit"
					disabled={isDisabled}
					size="sm"
					class={cn(
            "gap-2 min-w-[100px]",
            !isDisabled && "bg-gradient-to-r from-primary to-purple-600 hover:from-primary/90 hover:to-purple-600/90"
          )}
				>
					{#if inLoading}
						<Loader2 class="h-4 w-4 animate-spin" />
						Envoi...
					{:else}
						<Send class="h-4 w-4" />
						Envoyer
					{/if}
				</Button>
			</div>

			<!-- Indicateur de raccourci -->
			{#if !inLoading}
				<p class="text-xs text-muted-foreground text-center">
					Appuyez sur <kbd class="px-1 py-0.5 text-xs bg-muted rounded">Ctrl</kbd> +
					<kbd class="px-1 py-0.5 text-xs bg-muted rounded">Entrée</kbd> pour envoyer
				</p>
			{/if}
		</div>
	</form>
</div>