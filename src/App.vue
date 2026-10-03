<script setup>
import { ref, onBeforeUnmount } from 'vue'
import MovieCard from './components/MovieCard.vue'
import { fetchMovies } from './api.js'
import tmdbLogo from './assets/tmdb-logo.svg'

const draftKey = ref('')
const apiKey = ref('')
const query = ref('')
const activeQuery = ref('')
const movies = ref([])
const page = ref(1)
const totalPages = ref(0)
const totalResults = ref(0)
const loading = ref(false)
const error = ref('')
let controller
let requestId = 0

async function loadMovies(nextPage = 1, term = activeQuery.value) {
  const id = ++requestId
  controller?.abort()
  const currentController = new AbortController()
  controller = currentController
  let timedOut = false
  const timer = setTimeout(() => { timedOut = true; currentController.abort() }, 15000)
  loading.value = true
  error.value = ''
  movies.value = []
  try {
    const data = await fetchMovies({ apiKey: apiKey.value, query: term, page: nextPage, signal: currentController.signal })
    if (id !== requestId) return
    movies.value = data.results
    page.value = data.page
    totalPages.value = Math.min(data.total_pages, 500)
    totalResults.value = data.total_results
    activeQuery.value = term
  } catch (err) {
    if (id !== requestId) return
    error.value = timedOut ? 'Request timed out. Check your connection and retry.'
      : err.name === 'AbortError' ? ''
        : err.status !== undefined ? err.message
          : 'Could not reach TMDB. Check your connection or try again later.'
  } finally {
    clearTimeout(timer)
    if (id === requestId) loading.value = false
  }
}
function connect() {
  const key = draftKey.value.trim()
  if (!key) return
  apiKey.value = key
  draftKey.value = ''
  activeQuery.value = ''
  query.value = ''
  loadMovies(1, '')
}
function search() { loadMovies(1, query.value.trim()) }
function popular() { query.value = ''; loadMovies(1, '') }
function disconnect() {
  requestId++
  controller?.abort()
  apiKey.value = ''; draftKey.value = ''; query.value = ''; activeQuery.value = ''
  movies.value = []; error.value = ''; loading.value = false
  page.value = 1; totalPages.value = 0; totalResults.value = 0
}
onBeforeUnmount(() => { requestId++; controller?.abort() })
</script>

<template>
  <div class="app-shell" id="top">
    <header class="site-header">
      <a class="brand" href="#top" aria-label="Frame home"><span class="brand-mark">F</span><span>FRAME<span class="brand-dot">.</span></span></a>
      <nav aria-label="Main navigation"><a href="#movies">Discover</a><a href="#about">About</a></nav>
      <div class="header-right"><span class="live-dot"></span><span>CURATED BY YOU</span>
        <button v-if="apiKey" class="key-chip" type="button" @click="disconnect"><span class="key-status"></span> API key entered <span aria-hidden="true">↗</span></button>
      </div>
    </header>

    <main>
      <section class="hero" :class="{ 'hero-connected': apiKey }" aria-labelledby="hero-title">
        <div class="hero-grain" aria-hidden="true"></div>
        <div class="hero-content">
          <p class="eyebrow"><span class="eyebrow-line"></span>{{ apiKey ? 'YOUR PRIVATE SCREENING ROOM' : 'A PERSONAL CINEMA, ON DEMAND' }}</p>
          <h1 id="hero-title" v-if="!apiKey">The next great<br><em>film</em> is out there.</h1>
          <h1 id="hero-title" v-else>Find your next<br><em>favorite.</em></h1>
          <p class="hero-copy" v-if="!apiKey">A quieter way to find something worth watching.<br>Explore the world of film, one story at a time.</p>
          <p class="hero-copy" v-else>Explore the films people are talking about, or search for the one on your mind.</p>

          <form v-if="!apiKey" class="key-form" @submit.prevent="connect">
            <label for="tmdb-key">Connect your TMDB API key</label>
            <div class="input-shell"><span class="input-icon" aria-hidden="true">⌘</span><input id="tmdb-key" v-model="draftKey" type="password" placeholder="Paste your API key (v3)" autocomplete="off" spellcheck="false" required><button class="button-primary" type="submit" :disabled="!draftKey.trim()">Enter the cinema <span aria-hidden="true">↗</span></button></div>
            <p class="key-help"><span class="lock-icon" aria-hidden="true">▣</span> Your key stays in this tab and is sent only to TMDB. <a href="https://www.themoviedb.org/settings/api" target="_blank" rel="noopener">Get a free key <span aria-hidden="true">↗</span></a></p>
          </form>
          <template v-else>
            <form class="search-form" role="search" @submit.prevent="search">
              <label for="movie-query" class="visually-hidden">Search movie titles</label>
              <div class="input-shell search-shell"><span class="search-icon" aria-hidden="true">⌕</span><input id="movie-query" v-model="query" type="search" placeholder="Search a title, a feeling, a memory…" autocomplete="off"><button class="button-primary" :disabled="loading" type="submit">Search <span aria-hidden="true">↗</span></button></div>
            </form>
            <div class="hero-actions"><button class="text-action" type="button" :disabled="loading" @click="popular">↗ &nbsp; Back to popular</button><span class="action-separator"></span><button class="text-action" type="button" @click="disconnect">Change API key</button></div>
          </template>
        </div>
        <div class="hero-index" aria-hidden="true"><span>01</span><i></i><span>DISCOVERY</span></div>
        <div class="hero-decoration" aria-hidden="true"><div class="orbit orbit-one"></div><div class="orbit orbit-two"></div><div class="orbit orbit-three"></div><span class="deco-star">✳</span></div>
      </section>

      <section id="movies" class="catalog" aria-labelledby="catalog-title" :aria-busy="loading">
        <div class="catalog-topline"><span>THE COLLECTION <b> / </b> 2026</span><span>AN OPENING SCENE FOR EVERY MOOD</span></div>
        <div class="section-heading"><div><p class="eyebrow">{{ activeQuery ? 'SEARCHING THE ARCHIVE' : 'NOW IN THE SPOTLIGHT' }}</p><h2 id="catalog-title">{{ activeQuery ? `“${activeQuery}”` : 'Popular right now' }}<span class="heading-period">.</span></h2></div>
          <div v-if="apiKey && !loading && !error && movies.length" class="collection-note"><span class="live-dot"></span>{{ totalResults.toLocaleString() }} FILMS IN THE COLLECTION</div></div>
        <div v-if="!apiKey" class="welcome-panel"><div class="welcome-number">01</div><div><p class="eyebrow">READY WHEN YOU ARE</p><h3>First, take your seat.</h3><p>Connect your TMDB key above to bring the cinema to life. No account data is saved.</p></div><a href="https://www.themoviedb.org/settings/api" target="_blank" rel="noopener">HOW TO GET A KEY <span>↗</span></a></div>
        <template v-else-if="loading"><div class="section-loading" role="status"><span class="loader-ring"></span><div><strong>Setting the scene</strong><span>Finding films from TMDB…</span></div></div><div class="movie-grid skeleton-grid" aria-hidden="true"><div v-for="n in 6" :key="n" class="skeleton-card"><div class="skeleton-poster"></div><div class="skeleton-line"></div><div class="skeleton-line short"></div></div></div></template>
        <div v-else-if="error" class="status-panel error-panel" role="alert"><div class="status-symbol">!</div><div><p class="eyebrow">SOMETHING WENT OFF SCRIPT</p><h3>We couldn't reach the collection.</h3><p>{{ error }}</p><button class="button-secondary" @click="loadMovies(page, activeQuery)">Try again <span>↗</span></button></div></div>
        <template v-else>
          <div class="catalog-meta"><p class="result-count" role="status">{{ totalResults.toLocaleString() }} {{ totalResults === 1 ? 'film' : 'films' }} <span>·</span> page {{ page }} of {{ totalPages || 1 }}</p><span class="catalog-sort">SORTED BY <b>POPULARITY ↘</b></span></div>
          <div v-if="movies.length" class="movie-grid"><MovieCard v-for="(movie, index) in movies" :key="movie.id" :movie="movie" :index="index" /></div>
          <div v-else class="status-panel empty-panel"><div class="status-symbol">⌕</div><div><p class="eyebrow">NO MATCHES IN THIS REEL</p><h3>Nothing with that title. Yet.</h3><p>Try another search, or see what’s popular right now.</p><button class="button-secondary" @click="popular">Explore popular films <span>↗</span></button></div></div>
          <nav v-if="totalPages > 1" class="pagination" aria-label="Result pages"><button class="page-arrow" :disabled="page <= 1" @click="loadMovies(page - 1)"><span aria-hidden="true">←</span> Previous</button><div class="page-readout"><span class="page-current">{{ String(page).padStart(2, '0') }}</span><span class="page-divider"></span><span class="page-total">{{ String(totalPages).padStart(2, '0') }}</span></div><button class="page-arrow next" :disabled="page >= totalPages" @click="loadMovies(page + 1)">Next <span aria-hidden="true">→</span></button></nav>
        </template>
      </section>
    </main>
    <footer id="about" class="site-footer"><div class="footer-brand"><a class="brand" href="#top"><span class="brand-mark">F</span><span>FRAME<span class="brand-dot">.</span></span></a><p>A little less scrolling.<br>A lot more cinema.</p></div><div class="footer-info"><p class="eyebrow">ABOUT THIS PROJECT</p><p>This product uses the TMDB API but is not endorsed or certified by TMDB. Movie data and posters need an internet connection.</p></div><div class="footer-credit"><a href="https://www.themoviedb.org/" target="_blank" rel="noopener"><img :src="tmdbLogo" alt="The Movie Database (TMDB)" width="110"></a><span>MADE FOR THE LOVE OF FILM · 2026</span></div></footer>
  </div>
</template>
