<template>
  <div id="app">
    <div id="logo">
      <router-link to='/'>
       <img alt="Airdapt" height="80" src="./assets/Airdapt_logo.png">
      </router-link>
    </div>
    
    <MainHeader/>
    <tab-menu></tab-menu>
    <router-view/>
  </div>
</template>

<script>

import TabMenu from '@/components/TabMenu'
import MainHeader from '@/components/MainHeader'

export default {
  name: 'App',
  components: {
    TabMenu, MainHeader
  }

  
  
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 40px;
  font-size: 8px;
  
}
#logo {
  text-align: left;
  margin-top: -15px;
  
}
</style>