<script lang="ts">
	import type {PageProps} from './$types';

	let { form }: PageProps = $props();
</script>


<section
	class="container mx-auto px-4 py-8 max-w-md rounded border border-slate-200 shadow-sm"
	id="login"
>
	<form
		class="flex flex-col gap-2"
		method="POST"
	>
		<h1>S'inscrire :</h1>
		<div class="form-group">
			<label for="username">Username</label>
			<input id="username" name="username" required type="text">
		</div>
		<div class="form-group">
			<label for="password">Password</label>
			<input id="password" name="password" required type="password">
		</div>
		<button
			class="btn btn-primary w-full"
		>
			S'enregistrer
		</button>
	</form>

	<p>
		Vous avez déjà un compte ?
		<a class="text-blue-600 hover:text-blue-800 transition-colors" href="/login">se connecter !</a>
	</p>

	{#if form?.message}
		<div class={`callout callout-${form.type}`}>{form.message}</div>
	{/if}
</section>