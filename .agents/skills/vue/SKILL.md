---
name: vue
description: Guidance for Vue 3 Composition API, TypeScript, script setup, Pinia stores, Vue Router, and composables.
---

# Vue Skill Directive

<GUIDELINES>
1. **Composition API**: Use `<script setup lang="ts">` exclusively for all Vue components.
2. **Type Safety**: Define interfaces in `src/types/` for all props, emits, and store state.
3. **Pinia Stores**: Define Pinia stores using `defineStore()` with typed state, getters, and actions.
4. **Service Isolation**: Move HTTP calls to centralized service functions in `src/services/`.
5. **Component Reusability**: Keep UI components modular, accessible, and clean. Extract shared stateful logic into composables in `src/composables/`.
</GUIDELINES>
