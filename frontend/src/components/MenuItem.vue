<template>
     <button 
        @click="$emit('click')"
        :class="[
            'w-full flex items-center px-4 py-3 transition-all duration-200',
            'hover:bg-gray-100 rounded-lg mx-2',
            active ? 'bg-blue-50 text-blue-600' : 'text-gray-600',
            expanded ? 'justify-start' : 'justify-center'
        ]"
    >
        <span class="material-icons text-[20px] min-w-[24px]">{{ icon }}</span>
        <span 
            :class="[
                'transition-all duration-300 font-medium',
                expanded ? 'ml-4 opacity-100 w-auto' : 'w-0 opacity-0 overflow-hidden'
            ]"
        >
            {{ title }}
        </span>
    </button>
</template>

<script setup>
defineProps({
    icon: {
        type: String,
        required: true
    },
    title: {
        type: String,
        required: true
    },
    active: {
        type: Boolean,
        default: false
    },
    expanded: {
        type: Boolean,
        default: true
    }
})
</script> 