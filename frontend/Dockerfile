FROM node:18

WORKDIR /app

# Instalar curl para healthchecks
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar solo los archivos de dependencias para aprovechar la caché de Docker
COPY package.json ./

# Instalar dependencias
RUN npm install

# Copiar el resto del código
COPY . .

EXPOSE 5173

# Configurar Vite para escuchar en todas las interfaces
ENV VITE_HOST=0.0.0.0 