<script setup>
import { computed, ref, watch } from 'vue'
import { posterUrl } from '../api.js'
const props = defineProps({ movie: { type: Object, required: true }, index: { type: Number, default: 0 } })
const imageFailed = ref(false)
const imageUrl = computed(() => posterUrl(props.movie.poster_path))
const rating = computed(() => props.movie.vote_count > 0 ? Number(props.movie.vote_average).toFixed(1) : 'NR')
const year = computed(() => props.movie.release_date?.slice(0, 4) || 'Year unknown')
watch(imageUrl, () => { imageFailed.value = false })
</script>

<template>
  <article class="movie-card" :style="{ '--card-delay': `${Math.min(index, 12) * 45}ms` }">
    <a class="poster-link" :href="`https://www.themoviedb.org/movie/${movie.id}`" target="_blank" rel="noopener" :aria-label="`View ${movie.title} on TMDB`">
      <div class="poster-frame">
        <img v-if="imageUrl && !imageFailed" class="movie-poster" :src="imageUrl" :alt="`${movie.title} poster`" loading="lazy" width="500" height="750" @error="imageFailed = true">
        <div v-else class="poster-fallback"><span class="fallback-icon" aria-hidden="true">✳</span><span class="fallback-label">ARTWORK<br>UNAVAILABLE</span><strong>{{ movie.title }}</strong><span class="fallback-footer">FRAME / {{ year }}</span></div>
        <div class="poster-wash"></div><span class="poster-index">{{ String(index + 1).padStart(2, '0') }}</span><span class="poster-open" aria-hidden="true">↗</span>
        <span class="poster-rating" :aria-label="rating === 'NR' ? 'Not rated' : `Rated ${rating} out of 10`"><span class="rating-star" aria-hidden="true">✳</span>{{ rating }}</span>
      </div>
    </a>
    <div class="movie-info"><div class="movie-meta"><span>{{ year }}</span><span class="meta-dot"></span><span>FEATURE FILM</span></div><h3><a :href="`https://www.themoviedb.org/movie/${movie.id}`" target="_blank" rel="noopener">{{ movie.title }} <span aria-hidden="true">↗</span></a></h3><p class="overview">{{ movie.overview || 'A story still waiting to be told. No synopsis is available for this film.' }}</p></div>
  </article>
</template>
