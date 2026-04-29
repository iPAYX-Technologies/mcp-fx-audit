# Utilise l'image officielle Deno (puisque tu es sur Supabase Edge Functions)
FROM denoland/deno:alpine-1.42.1

# Dossier de travail
WORKDIR /app

# Copie les fichiers du projet
COPY . .

# Autorise les permissions réseau pour Deno
RUN deno cache main.ts

# Commande pour lancer le serveur MCP
CMD ["run", "--allow-net", "--allow-env", "main.ts"]
