<script lang="ts">
	import { page } from "$app/state";

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

</script>

<form
	method="POST"
	action={`/chat/${page.params.id}?/postMessage`}
	class="h-1/5 bg-white/60 backdrop-blur-sm rounded-2xl border border-slate-200/50 shadow-sm p-6"
>
	<div class="space-y-2">
		<div>
			<label class="block text-sm font-medium text-slate-600 mb-2" for="answer">Votre question</label>
			<textarea
				bind:value={answer}
				rows="2"
				name="answer"
				id="answer"
				placeholder="Tapez votre message ici..."
				class="w-full px-4 py-3 bg-white/80 border border-slate-200 outline-blue-200 rounded-xl focus:ring-2 focus:ring-blue-200 focus:border-blue-300 transition-all duration-200 resize-none text-slate-700 placeholder-slate-400"
			></textarea>
		</div>

		<div class="flex items-center justify-between">
			<div class="flex items-center space-x-4">
				{#if onToggleContext}
					<button
						onclick={onToggleContext}
						type="button"
						class="px-4 py-2 bg-gray-100/80 hover:bg-gray-200/80 text-gray-600 rounded-xl text-sm font-medium transition-all duration-200"
					>
						{showContext ? 'Masquer contexte' : 'Voir contexte'}
					</button>
				{/if}

				{#if error}
					<div class="bg-red-50/80 border border-red-200/50 text-red-600 px-4 py-2 rounded-xl text-sm backdrop-blur-sm">
						{error}
					</div>
				{/if}
			</div>

			<button
				type="submit"
				disabled={isDisabled}
				class="px-6 py-2.5 rounded-xl font-medium transition-all duration-200 focus:ring-2 focus:ring-blue-200 focus:ring-offset-2 {isDisabled
          ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
          : 'bg-gradient-to-r from-blue-400 to-purple-400 hover:from-blue-500 hover:to-purple-500 text-white shadow-sm'}"
			>
				{inLoading ? 'Envoi...' : 'Envoyer'}
			</button>
		</div>
	</div>
</form>