<script lang="ts">
	import type { ChatMessage } from '$lib/types';
	import Loader from "./loader.svelte";

	// Composants shadcn-svelte
	import { Badge } from "$lib/components/ui/badge";
	import { ScrollArea } from "$lib/components/ui/scroll-area";
	import { cn } from "$lib/utils";

	// Icônes pour différencier les rôles
	import { Bot, User, Settings } from "lucide-svelte";

	interface Props {
		name: string;
		messages: ChatMessage[];
		inLoading: boolean;
	}

	let { name, messages, inLoading }: Props = $props();

	// Auto-scroll vers le bas
	let scrollContainer: HTMLElement;

	$effect(() => {
		if (scrollContainer && (messages || inLoading)) {
			setTimeout(() => {
				scrollContainer.scrollTop = scrollContainer.scrollHeight;
			}, 100);
		}
	});

	// Fonction pour obtenir l'icône selon le rôle
	function getRoleIcon(role: string) {
		switch (role) {
			case 'assistant': return Bot;
			case 'user': return User;
			case 'system': return Settings;
			default: return User;
		}
	}

	// Fonction pour obtenir la variante du badge selon le rôle
	function getRoleBadgeVariant(role: string): "default" | "secondary" | "destructive" | "outline" {
		switch (role) {
			case 'assistant': return 'default';
			case 'user': return 'secondary';
			case 'system': return 'outline';
			default: return 'secondary';
		}
	}
</script>

<!-- Chat principal optimisé pour le layout -->
<div class="flex flex-col h-full bg-background border border-border rounded-lg overflow-hidden">
	<!-- Header du chat -->
	<div class="flex items-center justify-between p-4 border-b bg-muted/30">
		<h2 class="text-lg font-semibold text-foreground truncate">
			{name}
		</h2>
		<Badge variant="outline" class="text-xs">
			{messages.length} message{messages.length !== 1 ? 's' : ''}
		</Badge>
	</div>

	<!-- Zone des messages -->
	<ScrollArea class="flex-1 p-4" bind:viewport={scrollContainer}>
		<div class="space-y-4">
			{#each messages as message, index (index)}
				<div
					class={cn(
            "flex w-full animate-in slide-in-from-bottom-2 duration-300",
            (message.role === 'system' || message.role === 'assistant')
              ? 'justify-start'
              : 'justify-end'
          )}
				>
					<div
						class={cn(
              "flex flex-col gap-2 px-4 py-3 rounded-lg border max-w-[85%] min-w-[200px] shadow-sm",
              (message.role === 'system' || message.role === 'assistant')
                ? 'bg-muted/50 text-foreground border-border'
                : 'bg-primary/10 text-foreground border-primary/20 ml-auto'
            )}
					>
						<div class="flex items-center gap-2">
							<svelte:component
								this={getRoleIcon(message.role)}
								class="h-3 w-3 text-muted-foreground flex-shrink-0"
							/>
							<Badge
								variant={getRoleBadgeVariant(message.role)}
								class="text-xs font-medium capitalize"
							>
								{message.role}
							</Badge>
						</div>

						<div class="text-sm leading-relaxed prose prose-sm max-w-none dark:prose-invert prose-p:my-1 prose-headings:my-2">
							{@html message.message}
						</div>
					</div>
				</div>
			{/each}

			{#if inLoading}
				<div class="flex justify-start animate-in slide-in-from-bottom-2 duration-300">
					<div class="flex items-center gap-3 px-4 py-3 rounded-lg bg-muted/50 border border-border shadow-sm">
						<Bot class="h-3 w-3 text-muted-foreground" />
						<Loader />
					</div>
				</div>
			{/if}

			<!-- Espace pour éviter que le dernier message soit collé au bas -->
			<div class="h-4"></div>
		</div>
	</ScrollArea>
</div>