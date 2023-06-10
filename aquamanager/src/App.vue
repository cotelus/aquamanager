<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat&display=swap');

#app {
  font-family: Montserrat;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  padding-top: 60px;
}

html,
body {
  height: 100%;
  margin: 0;
  padding: 0;
}

@keyframes waveAnimation {
  0% {
    background-position: 0% 50%
  }

  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

@-webkit-keyframes waveAnimation {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.w-bg{
  height: 100%;
  justify-content: center;
  background-size: 300% 300%;
  background-image: linear-gradient(-45deg, rgba(62, 181, 155, 0.5) 0%, rgba(54, 155, 201, 0.5) 25%, rgba(62, 181, 155, 0.5) 51%, rgba(54, 155, 201, 0.5) 100%);
  -webkit-animation: waveAnimation 10s ease infinite;
  animation: waveAnimation 10s ease infinite;
}
</style>
