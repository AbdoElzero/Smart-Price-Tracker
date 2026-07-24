<template>
  <AuthLayout subtitle="سجّل الدخول لمتابعة أسعار منتجاتك المفضلة">
    <LoginForm />
  </AuthLayout>
</template>

<script setup>
import AuthLayout from "@/layouts/AuthLayout.vue";
import LoginForm from "@/components/auth/LoginForm.vue";
</script>
