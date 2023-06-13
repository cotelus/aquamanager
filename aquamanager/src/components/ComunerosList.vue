<template>
    <v-card class="mx-auto" max-width="500">
        <v-card-title class="text-white font-weight-bold secondary-bg">
            Comuneros
        </v-card-title>

        <v-divider></v-divider>

        <v-virtual-scroll :items="items" height="80vh" item-height="48">
            <template v-slot:default="{ item }">
                <v-list-item :title="`Fulanito de copas`" :subtitle="`Comunero nº${item}`">
                    <template v-slot:prepend>
                        <v-icon class="w-bg elevation-5" color="white">mdi-account</v-icon>
                    </template>

                    <template v-slot:append>
                        <v-btn icon="mdi-pencil" size="x-small" variant="tonal"></v-btn>
                    </template>
                </v-list-item>
            </template>
        </v-virtual-scroll>
    </v-card>
</template>

<script>
export default {
    data: () => ({
        items: Array.from({ length: 1000 }, (k, v) => v + 1),
    }),
}
</script>

<style>
.secondary-bg{
    background-color: #3eb59b;
}
</style>