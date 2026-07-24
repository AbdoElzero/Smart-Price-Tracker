<template>
  <div class="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
    <Navbar />
    <main class="flex-1">
      <router-view />
    </main>
    <Footer />
    <CompareBar />
  </div>
</template>

<script setup>
import Navbar from "@/components/layout/Navbar.vue";
import Footer from "@/components/layout/Footer.vue";
import CompareBar from "@/components/compare/CompareBar.vue";
</script>
