<template>
  <div class="w-full">
    <label
      v-if="label"
      :for="id"
      class="block mb-1.5 text-sm font-medium text-gray-700 dark:text-gray-300"
    >
      {{ label }}
    </label>
    <input
      :id="id"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :autocomplete="autocomplete"
      @input="$emit('update:modelValue', $event.target.value)"
      class="w-full px-4 py-2.5 rounded-lg border bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 transition-colors"
      :class="
        error
          ? 'border-danger focus:ring-danger/30'
          : 'border-gray-300 dark:border-gray-600 focus:ring-primary-500/30 focus:border-primary-500'
      "
    />
    <p v-if="error" class="mt-1.5 text-sm text-danger">{{ error }}</p>
  </div>
</template>

<script setup>
defineProps({
  modelValue: { type: String, default: "" },
  label: { type: String, default: "" },
  type: { type: String, default: "text" },
  placeholder: { type: String, default: "" },
  autocomplete: { type: String, default: "off" },
  error: { type: String, default: "" },
  id: { type: String, required: true },
});
defineEmits(["update:modelValue"]);
</script>
