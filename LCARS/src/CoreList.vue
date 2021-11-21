<template>
  <div
    class="list-post"
    data-observe-resizes
    data-breakpoints='{"SM": 760, "MD": 1200, "LG": 1600, "XL": 1900}'
  >
    <div class="lcars-title large" data-type="1">
      <span class="short-title">Posts</span>
      <span class="long-title">Posts</span>
    </div>
    <div>
      <div v-for="post in posts">
        <div class="title-row" data-v-32d132e8="">
          <span class="numbers-cell is-dot" data-v-32d132e8="" style="width: 45px;"></span>
          <span class="numbers-cell" data-v-32d132e8="">{{ post.id }}</span>
          <span class="numbers-cell" data-v-32d132e8="">{{ post.title }}</span>
          <span class="numbers-cell" data-v-32d132e8="">{{ post.date }}</span>
        </div>
        <div class="title-row white" v-html="post.body"></div>
        <hr/>
      </div>
    </div>

    <div class="galactic-noise">
      <canvas ref="noise"></canvas>
    </div>
    <div class="stars-container">
      <div
        v-for="(item, index) in labeledStars"
        :key="index"
        class="labeled-star-container"
        :style="{
          left: `calc(${item.left}% - 40px / 2)`,
          top: `calc(${item.top}% - 40px / 2)`,
        }"
      >
        <div
          class="labeled-star"
          :style="{
            width: item.size + 'px',
            height: item.size + 'px'
          }"
        >
        </div>
      </div>
      <div
        v-for="(item, index) in backgroundStars"
        :key="index"
        class="background-star"
        :style="{
          left: `calc(${item.left}% - ${item.size}px / 2)`,
          top: `calc(${item.top}% - ${item.size}px / 2)`,
          width: item.size + 'px',
          height: item.size + 'px'
        }"
      >
      </div>
    </div>
  </div>
</template>

<script>
import {
  makeRandomNumber,
  pickRandomWithoutReplacement,
  getRandomRange,
  getRandomInt,
  throttle
} from './utils'
import ForwardScanner from './ForwardScanner.vue'
import InspectBracket from './InspectBracket.vue'
import StarCoords from './StarCoords.vue'
import stars from './star-systems.json'
import DataService from "./services/DataService";

function testCollision (candidate, check, buffer = 0) {
  if (
    candidate.top > check.bottom + buffer ||
    candidate.right < check.left - buffer ||
    candidate.bottom < check.top - buffer ||
    candidate.left > check.right + buffer
  ) {
    return false
  }

  return true
}

export default {
  name: 'star-chart',
  props: {
    type: {
      default: 'nav',
      type: String,
      validator: function (value) {
        return ['nav', 'planet'].indexOf(value) !== -1
      }
    }
  },
  data() {
    const numbers = []
    for (let i = 0; i < 150; i++) {
      numbers.push(makeRandomNumber(4, true))
    }

    const backgroundStars = []
    for (let i = 0; i < 100; i++) {
      const star = {
        left: Math.random() * 100,
        top: Math.random() * 100,
        size: getRandomInt(1, 10)
      }
      backgroundStars.push(star)
    }
    
    const labeledStars = []
    const numberStars = getRandomInt(6, 18)
    for (let i = 0; i < numberStars; i++) {
      const star = {
        left: getRandomRange(2, 80),
        top: getRandomRange(10, 90),
        size: getRandomInt(8, 12),
        label: pickRandomWithoutReplacement(stars)
      }
      labeledStars.push(star)
    }

    return {
      posts: [],
      currentPost: null,
      currentIndex: -1,
      numbers,
      backgroundStars,
      labeledStars
    }
  },
  methods: {
    retrievePosts() {
      DataService.getAll()
        .then(response => {
          this.posts = response.data.items;
          console.log(response.data);
        })
        .catch(e => {
          console.log(e);
        })
    },
  },
  mounted() {
    this.retrievePosts();
    this.$nextTick(() => {

    })

    // Throttle the collision check when the window is resized to
    // limit calculations and layout thrashing
    // TODO: watch ResizeObserver on the element, instead of watching
    // window resize
    window.addEventListener('resize', this.throttledCheckLabelCollision)
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.throttledCheckLabelCollision)
  },
  components: {
    ForwardScanner,
    InspectBracket,
    StarCoords,
  }
}
</script>

<style scoped>

.white {
  color: white;
}

.star-chart {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.galactic-noise {
  position: absolute;
  width: 200%;
  height: 100%;
  left: 0;
  top: 0;
  animation-duration: 120s;
  animation-name: pan-right-and-back-3;
  animation-iteration-count: infinite;
  animation-timing-function: linear;
}

.galactic-noise canvas {
  width: 100%;
  height: 100%;
}

.grid-container {
  position: absolute;
  width: 240%;
  min-height: 120%;
  left: -10%;
  top: -10%;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(25vw, 1fr));
  grid-template-rows: repeat(auto-fit, minmax(25vw, 1fr));
  animation-duration: 120s;
  animation-name: pan-right-and-back-1;
  animation-iteration-count: infinite;
  animation-timing-function: linear;
}

.star-chart.SM .grid-container {
  grid-template-columns: repeat(auto-fit, minmax(20vw, 1fr));
  grid-template-rows: repeat(auto-fit, minmax(20vw, 1fr));
}

.star-chart.LG .grid-container {
  grid-template-columns: repeat(auto-fit, minmax(10vw, 1fr));
  grid-template-rows: repeat(auto-fit, minmax(10vw, 1fr));
}

.grid-item {
  border-left: 1px solid var(--lcars-color-a3);
  border-bottom: 1px solid var(--lcars-color-a3);
  padding: 10px;
  color: var(--lcars-color-a4);
  min-height: 20vw;
  opacity: 0.75;
}

.star-chart.LG .grid-item {
  min-height: 10vw;
}

.stars-container,
.label-container {
  position: absolute;
  width: 240%;
  height: 100%;
  top: 0;
  left: 0;
  animation-duration: 120s;
  animation-name: pan-right-and-back-2;
  animation-iteration-count: infinite;
  animation-timing-function: linear;
}

.background-star,
.labeled-star {
  position: absolute;
  border-radius: 50%;
}

.background-star {
  background-color: var(--lcars-color-a5);
}

.labeled-star-container {
  position: absolute;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.select {
  position: relative;
  width: 40px;
  height: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.select-left {
  position: absolute;
  left: 0;
  height: 75%;
  width: 10px;
  overflow: hidden;
}

.select-right {
  position: absolute;
  right: 0;
  height: 75%;
  width: 10px;
  overflow: hidden;
}

.select-bracket {
  position: absolute;
  height: 100%;
  width: 40px;
  border: 5px solid var(--lcars-color-b2);
  border-radius: 12px / 8px;
}

.select-left .select-bracket {
  left: 0;
}

.select-right .select-bracket {
  right: 0;
}

.labeled-star {
  background-color: var(--lcars-color-a1);
}

.label.collide {
  border: 1px solid red;
  opacity: 0;
  pointer-events: none;
}

.star-label {
  display: flex;
  position: absolute;
  height: 40px;
  align-items: center;
}

.label-text {
  color: var(--lcars-color-a8);
  text-transform: uppercase;
  white-space: nowrap;
  height: 40px;
  font-size: 2em;
  margin-left: 0.2em;
  /* Manual vertical alignment */
  line-height: 1.25;
}

/* By default, only show half of stars.
   As screen size gets bigger, progressively display more */
.background-star:nth-child(2n) {
  display: none;
}

.star-chart.MD .background-star:nth-child(2n) {
  display: inherit;
}

@keyframes pan-right-and-back-1 {
  from {
    transform: translateX(0);
  }

  48% {
    transform: translateX(-50%);
  }

  50% {
    transform: translateX(-50%);
  }

  98% {
    transform: translateX(0);
  }

  to {
    transform: translateX(0);
  }
}

@keyframes pan-right-and-back-2 {
  from {
    transform: translateX(0);
  }

  48% {
    transform: translateX(-40%);
  }

  50% {
    transform: translateX(-40%);
  }

  98% {
    transform: translateX(0);
  }

  to {
    transform: translateX(0);
  }
}

@keyframes pan-right-and-back-3 {
  from {
    transform: translateX(0);
  }

  48% {
    transform: translateX(-30%);
  }

  50% {
    transform: translateX(-30%);
  }

  98% {
    transform: translateX(0);
  }

  to {
    transform: translateX(0);
  }
}
</style>
