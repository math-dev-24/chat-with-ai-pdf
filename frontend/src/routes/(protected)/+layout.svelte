<script lang="ts">
	import { page } from "$app/state";
	import type { LayoutProps } from './$types';
	import { Button } from '$lib/components/ui/button';
	import { Power } from 'lucide-svelte';


	let { data, children }: LayoutProps = $props();


	const getStyle = (path: string) => {
		if (path === page.url.pathname) {
			return "text-purple-600 text-sm font-medium"
		}
		return "text-slate-600 hover:text-slate-800 transition-colors duration-200 text-sm font-medium"
	}

	let navItems = [
		{href: "/chat", label: "Chat"},
		{href: "/stat", label: "Stat"},
		{href: "/profil", label: "Profil"},
	]


</script>


<header class="bg-white/70 backdrop-blur-sm border-b border-slate-200/50 px-6 py-4">
	<ul class="flex gap-4 items-center">
		{#each navItems as item (item.href)}
			<li
				class={getStyle(item.href)}
			>
				<Button variant="link" href={item.href}>
					{item.label}
				</Button>
			</li>
		{/each}
		<li>
			<form action="/logout" method="POST">
				<Button variant="ghost" type="submit">
					<Power class="h-4" />
					<span>Déconnexion</span>
				</Button>
			</form>
		</li>
	</ul>
</header>

<main class="flex flex-col py-8 w-[95%] mx-auto">
	{@render children()}
</main>
