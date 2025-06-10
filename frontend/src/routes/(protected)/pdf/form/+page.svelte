<script lang="ts">
  import { Button } from '$lib/components/ui/button';
  import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '$lib/components/ui/card';
  import { writable } from 'svelte/store';
  import { base_url_api } from '$lib/const';

  let { data } = $props();
  const isUploading = writable(false);      
  const selectedFiles = writable<File[]>([]);

  const handleFileChange = (event: Event) => {
    const input = event.target as HTMLInputElement;
    if (input.files) {
      selectedFiles.set(Array.from(input.files));
    }
  };

  const uploadFiles = async (event: Event) => {
    event.preventDefault();
    const files = $selectedFiles;
    if (files.length === 0) {
      alert('Veuillez sélectionner au moins un fichier PDF');
      return;
    }

    if (!data.user) {
      alert('Utilisateur non connecté');
      return;
    }

    isUploading.set(true);
    const formData = new FormData();
    
    formData.append('user_id', data.user.id);
    
    files.forEach((file: File) => {
      formData.append('files', file);
    });

    try {
      const response = await fetch(`${base_url_api}/upload-documents`, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Erreur lors de l\'upload');
      }

      alert('Les fichiers ont été uploadés avec succès');

      selectedFiles.set([]);
      const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement;
      if (fileInput) fileInput.value = '';
    } catch (error) {
      console.error('Erreur upload:', error);
      alert('Une erreur est survenue lors de l\'upload des fichiers');
    } finally {
      isUploading.set(false);
    }
  };
</script>

<Card class="w-full max-w-2xl mx-auto mt-6">
  <CardHeader>
    <CardTitle>Upload de documents PDF</CardTitle>
    <CardDescription>
      Sélectionnez un ou plusieurs fichiers PDF à uploader
    </CardDescription>
  </CardHeader>
  <CardContent>
    <form onsubmit={uploadFiles} class="space-y-4">
      <div class="grid w-full max-w-sm items-center gap-1.5">
        <label
          for="pdf-files"
          class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
        >
          Fichiers PDF
        </label>
        <input
          type="file"
          id="pdf-files"
          accept=".pdf"
          multiple
          onchange={handleFileChange}
          class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
        />
      </div>

      {#if $selectedFiles.length > 0}
        <div class="mt-2">
          <p class="text-sm text-muted-foreground">
            {$selectedFiles.length} fichier(s) sélectionné(s)
          </p>
        </div>
      {/if}

      <Button type="submit" disabled={$isUploading}>
        {$isUploading ? 'Upload en cours...' : 'Uploader les fichiers'}
      </Button>
    </form>
  </CardContent>
</Card> 