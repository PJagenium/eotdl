<script>
	import { onMount } from "svelte";
	import retrieveModels from "$lib/models/retrieveModels";
	import Recent from "./Recent.svelte";

	export let tags;

	let data = null;
	onMount(async () => {
		data = await retrieveModels(fetch, 3);
	});
</script>

<Recent {data} title="Recent models" {tags} />
