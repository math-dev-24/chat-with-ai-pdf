<script lang="ts">
	import type { ChatMessage } from '$lib/types';
	import Loader from "./loader.svelte";

	import { Badge } from "$lib/components/ui/badge";
	import { cn } from "$lib/utils";

	import { Bot, User, Settings } from "lucide-svelte";

	interface Props {
		name: string;
		messages: ChatMessage[];
		inLoading: boolean;
	}

	let { name, messages, inLoading }: Props = $props();

	let messagesContainer: HTMLDivElement;

	$effect(() => {
		if (messagesContainer && (messages || inLoading)) {
			setTimeout(() => {
				messagesContainer.scrollTop = messagesContainer.scrollHeight;
			}, 100);
		}
	});

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
	<div class="flex-1 p-4 overflow-auto" bind:this={messagesContainer}>
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
							{#if message.role === 'assistant'}
								<Bot class="h-3 w-3 text-muted-foreground flex-shrink-0" />
							{:else if message.role === 'user'}
								<User class="h-3 w-3 text-muted-foreground flex-shrink-0" />
							{:else}
								<Settings class="h-3 w-3 text-muted-foreground flex-shrink-0" />
							{/if}
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
			<div class="h-4"></div>
		</div>
	</div>
</div>