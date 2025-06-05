<script lang="ts">
	// Composants shadcn-svelte
	import { Button } from "$lib/components/ui/button";
	import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "$lib/components/ui/card";
	import { Badge } from "$lib/components/ui/badge";
	import { Separator } from "$lib/components/ui/separator";

	// Icônes Lucide
	import {
		MessageCircle,
		FileText,
		Upload,
		Search,
		Zap,
		Brain,
		ArrowRight,
		Sparkles,
		Database,
		Bot
	} from "lucide-svelte";

	// Animation d'apparition progressive
	let mounted = $state(false);

	// Simule le montage du composant
	import { onMount } from 'svelte';
	onMount(() => {
		mounted = true;
	});

	// Fonctionnalités principales
	const features = [
		{
			icon: Upload,
			title: "Upload de PDFs",
			description: "Glissez-déposez vos documents PDF et laissez l'IA les analyser automatiquement"
		},
		{
			icon: Search,
			title: "Recherche intelligente",
			description: "Trouvez instantanément les informations dans vos documents grâce à l'IA"
		},
		{
			icon: MessageCircle,
			title: "Chat conversationnel",
			description: "Posez des questions naturelles et obtenez des réponses précises et contextuelles"
		}
	];

	// Statistiques fictives
	const stats = [
		{ label: "Documents traités", value: "1,247", icon: FileText },
		{ label: "Questions répondues", value: "8,932", icon: MessageCircle },
		{ label: "Utilisateurs actifs", value: "342", icon: Bot }
	];
</script>

<div class="min-h-screen bg-gradient-to-br from-background via-background to-muted/20">

	<!-- Hero Section -->
	<section class="container mx-auto px-4 py-16 text-center">
		<div class={`transition-all duration-1000 ${mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
			<Badge variant="secondary" class="mb-4">
				<Sparkles class="mr-1 h-3 w-3" />
				Powered by AI
			</Badge>

			<h1 class="text-4xl md:text-6xl font-bold tracking-tight mb-6">
				Chattez avec vos
				<span class="text-primary">documents PDF</span>
			</h1>

			<p class="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
				Transformez vos PDFs en conversations intelligentes. Posez des questions, obtenez des réponses instantanées et explorez vos documents comme jamais auparavant.
			</p>

			<div class="flex flex-col sm:flex-row gap-4 justify-center">
				<Button size="lg" href="/chat" class="gap-2">
					<MessageCircle class="h-5 w-5" />
					Commencer maintenant
				</Button>
				<Button size="lg" variant="outline" href="/dashboard" class="gap-2">
					<Database class="h-5 w-5" />
					Voir le dashboard
				</Button>
			</div>
		</div>
	</section>

	<!-- Features Section -->
	<section class="container mx-auto px-4 py-16">
		<div class="text-center mb-12">
			<h2 class="text-3xl font-bold mb-4">Fonctionnalités principales</h2>
			<p class="text-muted-foreground max-w-2xl mx-auto">
				Une suite d'outils alimentés par l'IA pour transformer votre façon d'interagir avec les documents
			</p>
		</div>

		<div class="grid md:grid-cols-3 gap-8">
			{#each features as feature, index}
				<Card class={`transition-all duration-700 hover:shadow-lg ${mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}
							style={`transition-delay: ${index * 200}ms`}>
					<CardHeader>
						<div class="flex items-center justify-center w-12 h-12 bg-primary/10 rounded-lg mb-4">
							<svelte:component this={feature.icon} class="h-6 w-6 text-primary" />
						</div>
						<CardTitle>{feature.title}</CardTitle>
					</CardHeader>
					<CardContent>
						<CardDescription class="text-base">
							{feature.description}
						</CardDescription>
					</CardContent>
				</Card>
			{/each}
		</div>
	</section>

	<!-- Stats Section -->
	<section class="bg-muted/50 py-16">
		<div class="container mx-auto px-4">
			<div class="text-center mb-12">
				<h2 class="text-3xl font-bold mb-4">En quelques chiffres</h2>
			</div>

			<div class="grid md:grid-cols-3 gap-8">
				{#each stats as stat, index}
					<div class={`text-center transition-all duration-700 ${mounted ? 'opacity-100 scale-100' : 'opacity-0 scale-95'}`}
							 style={`transition-delay: ${index * 150}ms`}>
						<div class="flex items-center justify-center w-16 h-16 bg-primary/10 rounded-full mx-auto mb-4">
							<svelte:component this={stat.icon} class="h-8 w-8 text-primary" />
						</div>
						<div class="text-3xl font-bold mb-2">{stat.value}</div>
						<div class="text-muted-foreground">{stat.label}</div>
					</div>
				{/each}
			</div>
		</div>
	</section>

	<!-- CTA Section -->
	<section class="container mx-auto px-4 py-16">
		<Card class="bg-gradient-to-r from-primary/10 via-primary/5 to-background border-primary/20">
			<CardContent class="text-center p-12">
				<Brain class="h-16 w-16 text-primary mx-auto mb-6" />
				<h2 class="text-3xl font-bold mb-4">Prêt à commencer ?</h2>
				<p class="text-muted-foreground mb-8 max-w-xl mx-auto">
					Uploadez votre premier PDF et découvrez la puissance de l'IA conversationnelle pour explorer vos documents.
				</p>
				<Button size="lg" href="/chat" class="gap-2">
					<Zap class="h-5 w-5" />
					Essayer maintenant
				</Button>
			</CardContent>
		</Card>
	</section>

	<!-- Footer -->
	<footer class="border-t bg-background/95 backdrop-blur">
		<div class="container mx-auto px-4 py-8">
			<div class="flex flex-col md:flex-row items-center justify-between">
				<div class="flex items-center gap-2 mb-4 md:mb-0">
					<div class="flex items-center justify-center w-6 h-6 bg-primary rounded">
						<Bot class="h-4 w-4 text-primary-foreground" />
					</div>
					<span class="font-semibold">ChatPDF</span>
				</div>
				<p class="text-sm text-muted-foreground">
					© 2025 ChatPDF. Alimenté par l'intelligence artificielle.
				</p>
			</div>
		</div>
	</footer>
</div>