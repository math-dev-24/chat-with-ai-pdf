<script lang="ts">
	import MainChat from '$lib/components/chat/main-chat.svelte';
	import InputChat from '$lib/components/chat/input-chat.svelte';
	import CardConv from '$lib/components/chat/conversation/card.svelte';
	import NewConversation from '$lib/components/chat/new-conversation.svelte';


	import { Card, CardContent, CardHeader, CardTitle, CardFooter } from "$lib/components/ui/card";
	import { Button } from '$lib/components/ui/button';
	import { Badge } from '$lib/components/ui/badge';
	import { ScrollArea } from '$lib/components/ui/scroll-area';
	import { Separator } from '$lib/components/ui/separator';
	import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetDescription } from "$lib/components/ui/sheet";

	// Icônes Lucide
	import {
		User,
		MessageCircle,
		Plus,
		Settings,
		LogOut,
		Menu,
		X,
		FileText
	} from 'lucide-svelte';

	import type { StateChat } from '$lib/types';
	import { cn } from '$lib/utils';
	import { goto } from '$app/navigation';

	let { data } = $props();

	let isLoading = $state(true);

	$effect(() => {
		if (data) {
			isLoading = false;
			if (!data.isNew && !data.actual_conversation) {
				goto('/chat/new');
			}
		}
	});

	let stateChat = $state<StateChat>({
		answer: "",
		inLoading: false,
		errors: [],
		showContext: false
	});

	let sidebarOpen = $state(false);

	function toggleContext() {
		stateChat.showContext = !stateChat.showContext;
	}

	function toggleSidebar() {
		sidebarOpen = !sidebarOpen;
	}

	function closeSidebar() {
		sidebarOpen = false;
	}
</script>

<svelte:head>
	<title>Chat : {data?.actual_conversation?.name || 'Nouvelle conversation'}</title>
</svelte:head>

<div class="flex h-screen bg-background">
	<!-- Overlay mobile -->
	{#if sidebarOpen}
		<Button
			class="fixed inset-0 z-40 bg-background/80 backdrop-blur-sm lg:hidden"
			variant="ghost"
			onclick={closeSidebar}
			onkeydown={(e: KeyboardEvent) => e.key === 'Enter' && closeSidebar()}
			role="button"
		>
			<X class="h-4 w-4" />
		</Button>
	{/if}

	<!-- Sidebar conversations -->
	<aside class={cn(
    "fixed inset-y-0 left-0 z-50 w-80 transform transition-transform duration-200 ease-in-out lg:relative lg:translate-x-0 lg:z-0",
    sidebarOpen ? "translate-x-0" : "-translate-x-full"
  )}>
		<Card class="h-full rounded-none border-r border-l-0 border-t-0 border-b-0 bg-muted/30">
			<!-- Header sidebar -->
			<CardHeader class="pb-4">
				<div class="flex items-center justify-between">
					<CardTitle class="flex items-center gap-2 text-lg">
						<MessageCircle class="h-5 w-5 text-primary" />
						Conversations
					</CardTitle>
					<!-- Bouton fermer mobile -->
					<Button
						variant="ghost"
						size="sm"
						class="lg:hidden h-8 w-8 p-0"
						onclick={closeSidebar}
					>
						<X class="h-4 w-4" />
					</Button>
				</div>

				<!-- Bouton nouvelle conversation -->
				<Button
					class="w-full gap-2 mt-4"
					variant="outline"
					href="/chat/new"
				>
					<Plus class="h-4 w-4" />
					Nouvelle conversation
				</Button>
			</CardHeader>

			<!-- Liste des conversations -->
			<CardContent class="flex-1 px-4 pb-4">
				<ScrollArea class="h-[calc(100vh-280px)]">
					<ul class="space-y-1">
						{#each data?.list_conversations || [] as conversation (conversation.id)}
							<CardConv {conversation} />
						{/each}
					</ul>
				</ScrollArea>
			</CardContent>

			<Separator class="mx-4" />

			<!-- Footer avec profil utilisateur -->
			<CardFooter class="pt-4">
				<div class="w-full space-y-3">
					<!-- Info utilisateur -->
					<div class="flex items-center gap-3 p-3 rounded-lg bg-background/50">
						<div class="flex items-center justify-center w-8 h-8 bg-primary/10 rounded-full">
							<User class="h-4 w-4 text-primary" />
						</div>
						<div class="flex-1 min-w-0">
							<p class="text-sm font-medium truncate">
								{data?.user?.username || "Utilisateur"}
							</p>
							<p class="text-xs text-muted-foreground">
								{data?.list_conversations?.length || 0} conversation{(data?.list_conversations?.length || 0) !== 1 ? 's' : ''}
							</p>
						</div>
					</div>

					<!-- Actions utilisateur -->
					<div class="flex gap-2">
						<Button
							variant="outline"
							size="sm"
							class="flex-1 gap-2"
							href="/profil"
						>
							<Settings class="h-4 w-4" />
							Profil
						</Button>
						<Button
							variant="outline"
							size="sm"
							class="flex-1 gap-2"
							href="/logout"
						>
							<LogOut class="h-4 w-4" />
							Déconnexion
						</Button>
					</div>
				</div>
			</CardFooter>
		</Card>
	</aside>

	<!-- Zone principale de chat -->
	<main class="flex-1 flex flex-col min-w-0">
		<!-- Header mobile avec menu burger -->
		<header class="lg:hidden flex items-center justify-between p-4 border-b bg-background/95 backdrop-blur">
			<Button
				variant="ghost"
				size="sm"
				onclick={toggleSidebar}
				class="gap-2"
			>
				<Menu class="h-4 w-4" />
				Menu
			</Button>

			<div class="flex items-center gap-2">
				<Badge variant="secondary" class="text-xs">
					{data?.actual_conversation?.name || 'Nouvelle conversation'}
				</Badge>
			</div>
		</header>

		<!-- Zone de chat -->
		<div class="flex-1 flex flex-col overflow-hidden p-4 gap-3">
			{#if isLoading}
				<div class="flex-1 flex items-center justify-center">
					<div class="animate-pulse">Chargement...</div>
				</div>
			{:else if data?.isNew}
				<div class="flex-1 flex items-center justify-center">
					<NewConversation />
				</div>
			{:else}
				<div class="flex-1 min-h-0">
					<MainChat
						name={data?.actual_conversation?.name || 'Nouvelle conversation'}
						messages={data?.actual_conversation?.messages || []}
						inLoading={stateChat.inLoading}
					/>
				</div>
				<div class="flex-shrink-0">
					<InputChat
						answer={stateChat.answer}
						inLoading={stateChat.inLoading}
						error={stateChat.errors[0] || ''}
						showContext={stateChat.showContext}
						onToggleContext={toggleContext}
					/>
				</div>
			{/if}
		</div>

		<!-- Sheet pour afficher le contexte -->
		<Sheet bind:open={stateChat.showContext} onOpenChange={(value) => stateChat.showContext = value}>
			<SheetContent side="right" class="!min-w-[800px]">
				<SheetHeader>
					<SheetTitle class="flex items-center gap-2">
						<FileText class="h-5 w-5" />
						Contexte de la conversation
					</SheetTitle>
					<SheetDescription>
						Documents et informations utilisés pour générer les réponses
					</SheetDescription>
				</SheetHeader>
				<div class="mt-6">
					<ScrollArea class="h-[calc(100vh-200px)]">
						{#if data?.actual_conversation && data?.actual_conversation?.contexts && data?.actual_conversation?.contexts.length === 0}
							<div class="text-center text-muted-foreground py-8">
								Aucun contexte disponible
							</div>
						{:else}
							<div class="space-y-4">
								{#each data?.actual_conversation?.contexts || [] as context}
									{#each context.content.split('---') as item}
										{#if item.includes('[Source:')}
										<Card>
											<CardContent class="p-4">
												<h3 class="text-sm font-medium mb-2">{item.split(']')[0].replace('[Source: ', '')}</h3>
												<p class="text-sm">{item.split(']')[1]}</p>
											</CardContent>
											<CardFooter class="flex justify-between items-center">
												<span class="text-xs text-muted-foreground">{context.id}</span>
												<span class="text-xs text-muted-foreground">{new Date(context.createdAt).toLocaleDateString()}</span>
											</CardFooter>
										</Card>
										{/if}
									{/each}
								{/each}
							</div>
						{/if}
					</ScrollArea>
				</div>
			</SheetContent>
		</Sheet>
	</main>
</div>