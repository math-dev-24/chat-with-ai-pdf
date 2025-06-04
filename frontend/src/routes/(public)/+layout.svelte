<script lang="ts">
	let { data, children } = $props();
</script>


<header class="py-2 px-6">
	<nav>
		<ul class="flex gap-4">
			<li><a href="/">Home</a></li>
			{#if data.user}
				<li><a href="/chat">Chat</a></li>
				<li><a href="/profil">Profil</a></li>
			{:else}
				<li><a href="/login">Login</a></li>
				<li><a href="/register">Register</a></li>
			{/if}
		</ul>
	</nav>
</header>

{@render children()}
