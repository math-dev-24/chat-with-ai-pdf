<script lang="ts">
	import type { PageProps } from './$types';

	// Composants shadcn-svelte
	import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "$lib/components/ui/card";
	import { Alert, AlertDescription, AlertTitle } from "$lib/components/ui/alert";
	import { Input } from "$lib/components/ui/input";
	import { Label } from "$lib/components/ui/label";
	import { Button } from '$lib/components/ui/button';
	import { Separator } from '$lib/components/ui/separator';
	import { Badge } from '$lib/components/ui/badge';

	// Icônes Lucide
	import {
		User,
		Lock,
		UserPlus,
		AlertCircle,
		Bot,
		ArrowLeft,
		Eye,
		EyeOff,
		Check,
		X,
		Shield
	} from 'lucide-svelte';

	let { form }: PageProps = $props();

	// États pour afficher/masquer les mots de passe
	let showPassword = $state(false);
	let showConfirmPassword = $state(false);

	// État de loading pour le formulaire
	let isLoading = $state(false);

	// Valeurs des champs pour validation en temps réel
	let username = $state('');
	let password = $state('');
	let confirmPassword = $state('');

	// Validation en temps réel
	let usernameValid = $derived(username.length >= 3);
	let passwordValid = $derived(password.length >= 6);
	let passwordsMatch = $derived(password && confirmPassword && password === confirmPassword);

	// Fonctions pour validation regex
	function hasUppercase(str: string): boolean {
		return /[A-Z]/.test(str);
	}

	function hasNumber(str: string): boolean {
		return /[0-9]/.test(str);
	}

	let formValid = $derived(usernameValid && passwordValid && passwordsMatch);

	function togglePasswordVisibility() {
		showPassword = !showPassword;
	}

	function toggleConfirmPasswordVisibility() {
		showConfirmPassword = !showConfirmPassword;
	}

	function handleSubmit() {
		isLoading = true;
		// Le loading sera réinitialisé par la navigation ou l'erreur
	}
</script>

<div class="flex items-center justify-center bg-gradient-to-br from-background via-background to-muted/20 p-4 mt-6">
	<div class="w-full max-w-md space-y-6">

		<Card class="shadow-lg border-border/50">
			<CardHeader class="space-y-1 text-center pb-4">
				<CardTitle class="text-xl flex items-center justify-center gap-2">
					<UserPlus class="h-5 w-5 text-primary" />
					Inscription
				</CardTitle>
				<CardDescription>
					Remplissez les informations ci-dessous pour créer votre compte
				</CardDescription>
			</CardHeader>

			<CardContent class="space-y-4">
				<form
					class="space-y-4"
					method="POST"
					onsubmit={handleSubmit}
				>
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
								placeholder="Choisissez un nom d'utilisateur"
								class="pl-10 pr-10 bg-background"
								bind:value={username}
								required
								disabled={isLoading}
							/>
							{#if username}
								<div class="absolute right-3 top-1/2 transform -translate-y-1/2">
									{#if usernameValid}
										<Check class="h-4 w-4 text-green-500" />
									{:else}
										<X class="h-4 w-4 text-red-500" />
									{/if}
								</div>
							{/if}
						</div>
						{#if username && !usernameValid}
							<p class="text-xs text-red-500">Le nom d'utilisateur doit contenir au moins 3 caractères</p>
						{/if}
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
								placeholder="Choisissez un mot de passe"
								class="pl-10 pr-10 bg-background"
								bind:value={password}
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
						{#if password && !passwordValid}
							<p class="text-xs text-red-500">Le mot de passe doit contenir au moins 6 caractères</p>
						{/if}
					</div>

					<!-- Champ Confirmation Password -->
					<div class="space-y-2">
						<Label for="confirm-password" class="text-sm font-medium">
							Confirmer le mot de passe
						</Label>
						<div class="relative">
							<Shield class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
							<Input
								id="confirm-password"
								name="confirm-password"
								type={showConfirmPassword ? "text" : "password"}
								placeholder="Confirmez votre mot de passe"
								class="pl-10 pr-10 bg-background"
								bind:value={confirmPassword}
								required
								disabled={isLoading}
							/>
							<Button
								type="button"
								variant="ghost"
								size="sm"
								class="absolute right-1 top-1/2 transform -translate-y-1/2 h-8 w-8 p-0 hover:bg-transparent"
								onclick={toggleConfirmPasswordVisibility}
								disabled={isLoading}
							>
								{#if showConfirmPassword}
									<EyeOff class="h-4 w-4 text-muted-foreground" />
								{:else}
									<Eye class="h-4 w-4 text-muted-foreground" />
								{/if}
							</Button>
						</div>
						{#if confirmPassword && !passwordsMatch}
							<p class="text-xs text-red-500">Les mots de passe ne correspondent pas</p>
						{/if}
					</div>

					<!-- Indicateurs de force du mot de passe -->
					{#if password}
						<div class="space-y-2">
							<div class="flex gap-1">
								<Badge variant={password.length >= 6 ? "default" : "secondary"} class="text-xs">
									{password.length >= 6 ? "✓" : "○"} 6+ caractères
								</Badge>
								<Badge variant={hasUppercase(password) ? "default" : "secondary"} class="text-xs">
									{hasUppercase(password) ? "✓" : "○"} Majuscule
								</Badge>
								<Badge variant={hasNumber(password) ? "default" : "secondary"} class="text-xs">
									{hasNumber(password) ? "✓" : "○"} Chiffre
								</Badge>
							</div>
						</div>
					{/if}

					<!-- Bouton de soumission -->
					<Button
						type="submit"
						class="w-full gap-2 mt-6"
						disabled={!formValid || isLoading}
					>
						{#if isLoading}
							<div class="h-4 w-4 animate-spin rounded-full border-2 border-background border-t-transparent"></div>
							Création du compte...
						{:else}
							<UserPlus class="h-4 w-4" />
							Créer mon compte
						{/if}
					</Button>
				</form>
			</CardContent>

			<!-- Message d'erreur -->
			{#if form?.message}
				<CardContent class="pt-0">
					<Alert variant="destructive" class="animate-in slide-in-from-top-2 duration-300">
						<AlertCircle class="h-4 w-4" />
						<AlertTitle>Erreur lors de l'inscription</AlertTitle>
						<AlertDescription>
							{form.message}
						</AlertDescription>
					</Alert>
				</CardContent>
			{/if}

			<CardFooter class="flex flex-col space-y-4 pt-6">
				<Separator />

				<!-- Lien vers la connexion -->
				<div class="text-center text-sm space-y-2">
					<p class="text-muted-foreground">
						Vous avez déjà un compte ?
					</p>
					<Button variant="outline" href="/login" class="gap-2">
						<ArrowLeft class="h-4 w-4" />
						Se connecter
					</Button>
				</div>

				<!-- Conditions d'utilisation -->
				<div class="text-center text-xs text-muted-foreground">
					<p>En créant un compte, vous acceptez nos</p>
					<div class="flex justify-center gap-1">
						<Button variant="link" href="/terms" class="text-xs p-0 h-auto">
							Conditions d'utilisation
						</Button>
						<span>et notre</span>
						<Button variant="link" href="/privacy" class="text-xs p-0 h-auto">
							Politique de confidentialité
						</Button>
					</div>
				</div>
			</CardFooter>
		</Card>

		<!-- Footer -->
		<div class="text-center text-xs text-muted-foreground">
			<p>© 2025 ChatPDF. Tous droits réservés.</p>
		</div>
	</div>
</div>