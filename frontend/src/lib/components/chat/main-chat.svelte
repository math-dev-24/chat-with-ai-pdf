<script lang="ts">
	import type { ChatMessage } from '$lib/types';
	import Loader from "./loader.svelte";

	// Composants shadcn-svelte
	import { Card, CardContent, CardHeader, CardTitle } from "$lib/components/ui/card";
	import { Badge } from "$lib/components/ui/badge";
	import { ScrollArea } from "$lib/components/ui/scroll-area";
	import { Separator } from "$lib/components/ui/separator";
	import { cn } from "$lib/utils";

	// Icônes pour différencier les rôles
	import { Bot, User, Settings } from "lucide-svelte";

	interface Props {
		name: string;
		messages: ChatMessage[];
		inLoading: boolean;
	}

	let { name, messages, inLoading }: Props = $props();

	// Fonction pour obtenir l'icône selon le rôle
	function getRoleIcon(role: string) {
		switch (role) {
			case 'assistant':
				return Bot;
			case 'user':
				return User;
			case 'system':
				return Settings;
			default:
				return User;
		}
	}

	// Fonction pour obtenir la variante du badge selon le rôle
	function getRoleBadgeVariant(role: string): "default" | "secondary" | "destructive" | "outline" {
		switch (role) {
			case 'assistant':
				return 'default';
			case 'user':
				return 'secondary';
			case 'system':
				return 'outline';
			default:
				return 'secondary';
		}
	}
</script>

<Card class="mb-6 flex flex-col h-4/5 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
	<CardHeader class="pb-3">
		<CardTitle class="text-xl text-center text-muted-foreground font-medium">
			{name}
		</CardTitle>
		<Separator class="mt-2" />
	</CardHeader>

	<CardContent class="flex-1 p-0">
		<ScrollArea class="h-full px-6">
			<div class="space-y-4 py-4">
				{#each messages as message, index (index)}
					<div
						class={cn(
              "flex w-full",
              (message.role === 'system' || message.role === 'assistant')
                ? 'justify-start'
                : 'justify-end'
            )}
					>
						<div
							class={cn(
                "flex flex-col gap-2 px-4 py-3 rounded-xl border max-w-[80%] min-w-[200px]",
                (message.role === 'system' || message.role === 'assistant')
                  ? 'bg-muted/50 text-foreground border-border'
                  : 'bg-primary/10 text-foreground border-primary/20'
              )}
						>
							<div class="flex items-center gap-2">
								<svelte:component
									this={getRoleIcon(message.role)}
									class="h-3 w-3 text-muted-foreground"
								/>
								<Badge
									variant={getRoleBadgeVariant(message.role)}
									class="text-xs font-medium capitalize"
								>
									{message.role}
								</Badge>
							</div>

							<div class="text-sm leading-relaxed prose prose-sm max-w-none dark:prose-invert">
								{@html message.message}
							</div>
						</div>
					</div>
				{/each}

				{#if inLoading}
					<div class="flex justify-start">
						<div class="flex items-center gap-2 px-4 py-3 rounded-xl bg-muted/50 border">
							<Bot class="h-3 w-3 text-muted-foreground" />
							<Loader />
						</div>
					</div>
				{/if}
			</div>
		</ScrollArea>
	</CardContent>
</Card>