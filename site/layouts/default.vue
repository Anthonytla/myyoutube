<template>
  <div>
    <Navbar/>
    <nuxt :key="$route.fullPath"/>
  </div>
</template>

<script>
import Navbar from '~/components/Navbar'

export default {
  components: {
    Navbar
  }
}
</script>