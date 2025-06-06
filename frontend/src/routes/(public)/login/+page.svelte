<script lang="ts">
	import type { PageProps } from './$types';
	import { enhance } from '$app/forms';

	import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "$lib/components/ui/card";
	import { Alert, AlertDescription, AlertTitle } from "$lib/components/ui/alert";
	import { Input } from "$lib/components/ui/input";
	import { Label } from "$lib/components/ui/label";
	import { Button } from '$lib/components/ui/button';
	import { Separator } from '$lib/components/ui/separator';

	import {
		User,
		Lock,
		LogIn,
		AlertCircle,
		ArrowRight,
		Eye,
		EyeOff
	} from 'lucide-svelte';

	let { data, form }: PageProps = $props();

	let showPassword = $state(false);

	let isLoading = $state(false);

	function togglePasswordVisibility() {
		showPassword = !showPassword;
	}

</script>

<svelte:head>
	<title>Se connecter !</title>
</svelte:head>

<div class="flex items-center justify-center bg-gradient-to-br from-background via-background to-muted/20 p-4 mt-6">
	<div class="w-full max-w-md space-y-6">

		<Card class="shadow-lg border-border/50">
			<CardHeader class="space-y-1 text-center pb-4">
				<CardTitle class="text-xl flex items-center justify-center gap-2">
					<LogIn class="h-5 w-5 text-primary" />
					Connexion
				</CardTitle>
				<CardDescription>
					Saisissez vos identifiants pour accéder à votre compte
				</CardDescription>
			</CardHeader>

			<CardContent class="space-y-4">
				<form
					class="space-y-4"
					method="POST"
					use:enhance={() => {
						isLoading = true
						return async({update}) => {
							await update();
							isLoading = false
						}
					}}
				>
					<!-- Pour redirect si besoin -->
					<Input type="hidden" value={data.from} name="from" id="from" />

					<!-- Champ Username -->
					<div class="space-y-2">
						<Label for="username" class="text-sm font-medium">
							Nom d'utilisateur
						</Label>
						<div class="relative">
							<User class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
							<Input
								id="username"
								name="username"
								type="text"
								placeholder="Votre nom d'utilisateur"
								class="pl-10 bg-background"
								required
								disabled={isLoading}
							/>
						</div>
					</div>

					<!-- Champ Password -->
					<div class="space-y-2">
						<Label for="password" class="text-sm font-medium">
							Mot de passe
						</Label>
						<div class="relative">
							<Lock class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
							<Input
								id="password"
								name="password"
								type={showPassword ? "text" : "password"}
								placeholder="Votre mot de passe"
								class="pl-10 pr-10 bg-background"
								required
								disabled={isLoading}
							/>
							<Button
								type="button"
								variant="ghost"
								size="sm"
								class="absolute right-1 top-1/2 transform -translate-y-1/2 h-8 w-8 p-0 hover:bg-transparent"
								onclick={togglePasswordVisibility}
								disabled={isLoading}
							>
								{#if showPassword}
									<EyeOff class="h-4 w-4 text-muted-foreground" />
								{:else}
									<Eye class="h-4 w-4 text-muted-foreground" />
								{/if}
							</Button>
						</div>
					</div>

					<!-- Bouton de soumission -->
					<Button
						type="submit"
						class="w-full gap-2 mt-6"
						disabled={isLoading}
					>
						{#if isLoading}
							<div class="h-4 w-4 animate-spin rounded-full border-2 border-background border-t-transparent"></div>
							Connexion en cours...
						{:else}
							<LogIn class="h-4 w-4" />
							Se connecter
						{/if}
					</Button>
				</form>
			</CardContent>

			<!-- Message d'erreur -->
			{#if form?.message}
				<CardContent class="pt-0">
					<Alert variant="destructive" class="animate-in slide-in-from-top-2 duration-300">
						<AlertCircle class="h-4 w-4" />
						<AlertTitle>Erreur de connexion</AlertTitle>
						<AlertDescription>
							{form.message}
						</AlertDescription>
					</Alert>
				</CardContent>
			{/if}

			<CardFooter class="flex flex-col space-y-4 pt-6">
				<Separator />

				<!-- Lien vers l'inscription -->
				<div class="text-center text-sm space-y-2">
					<p class="text-muted-foreground">
						Vous n'avez pas encore de compte ?
					</p>
					<Button variant="outline" href="/register" class="gap-2">
						Créer un compte
						<ArrowRight class="h-4 w-4" />
					</Button>
				</div>
			</CardFooter>
		</Card>

		<!-- Footer -->
		<div class="text-center text-xs text-muted-foreground">
			<p>© 2025 ChatPDF. Tous droits réservés.</p>
		</div>
	</div>
</div>