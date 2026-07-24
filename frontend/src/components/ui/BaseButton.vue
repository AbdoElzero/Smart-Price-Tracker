<template>
  <button
    :type="type"
    :disabled="loading || disabled"
    class="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg font-semibold text-white bg-primary-600 hover:bg-primary-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
  >
    <svg
      v-if="loading"
      class="animate-spin h-5 w-5"
      viewBox="0 0 24 24"
      fill="none"
    >
      <circle
        class="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        stroke-width="4"
      />
      <path
        class="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
      />
    </svg>
    <slot v-else />
  </button>
</template>

<script setup>
defineProps({
  type: { type: String, default: "submit" },
  loading: { type: Boolean, default: false },
  disabled: { type: Boolean, default: false },
});
</script>
