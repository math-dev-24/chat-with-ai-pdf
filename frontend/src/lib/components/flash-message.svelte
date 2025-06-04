<script lang="ts">
	import { onMount } from 'svelte';
	import type { FlashMessage } from '$lib/services';

	interface Props {
		flashMessage: FlashMessage | null;
	}

	let { flashMessage }: Props = $props();

	let isVisible = $state(false);
	let isAnimating = $state(false);

	const icons = {
		success: '✅',
		error: '❌',
		warning: '⚠️',
		info: 'ℹ️'
	};

	const getMessageClasses = (type: string) => {
		const baseClasses = "flex items-center px-4 py-3 rounded-lg border shadow-sm";

		switch (type) {
			case 'success':
				return `${baseClasses} bg-green-50 border-green-200 text-green-800`;
			case 'error':
				return `${baseClasses} bg-red-50 border-red-200 text-red-800`;
			case 'warning':
				return `${baseClasses} bg-yellow-50 border-yellow-200 text-yellow-800`;
			case 'info':
				return `${baseClasses} bg-blue-50 border-blue-200 text-blue-800`;
			default:
				return `${baseClasses} bg-gray-50 border-gray-200 text-gray-800`;
		}
	};

	onMount(() => {
		if (flashMessage) {
			setTimeout(() => {
				isVisible = true;
				isAnimating = true;
			}, 100);

			setTimeout(() => {
				hideMessage();
			}, 3000);
		}
	});

	function hideMessage() {
		isAnimating = false;
		setTimeout(() => {
			isVisible = false;
		}, 300);
	}
</script>

<!-- Container fixe en bas à droite -->
{#if flashMessage && isVisible}
	<div class="fixed bottom-6 right-6 z-[60] w-full max-w-sm">
		<div
			class="transition-all duration-300 ease-out {isAnimating ? 'translate-x-0 opacity-100' : 'translate-x-4 opacity-0'} {getMessageClasses(flashMessage.type)}"
		>
			<!-- Icon -->
			<span class="text-lg mr-3 flex-shrink-0">
                {icons[flashMessage.type]}
            </span>

			<!-- Message -->
			<div class="flex-1">
				<p class="font-medium text-sm">
					{flashMessage.message}
				</p>
			</div>

			<!-- Bouton fermer -->
			<button
				onclick={hideMessage}
				class="ml-3 flex-shrink-0 text-lg opacity-70 hover:opacity-100 transition-opacity"
				aria-label="Fermer le message"
			>
				✕
			</button>
		</div>
	</div>
{/if}

<style>
    :global(.flash-message-container) {
        z-index: 60;
    }
</style>