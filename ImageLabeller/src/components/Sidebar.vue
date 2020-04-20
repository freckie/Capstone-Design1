<template>
  <div class="sidebar">
    <!-- Side bar -->
    <v-navigation-drawer
      app
      dark
      width="220"
      permanent
    >

      <!-- Header -->
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="title nonselectable-text">
            {{ title }}
          </v-list-item-title>
          <v-list-item-subtitle class="nonselectable-text">
            {{ subtitle }}
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>

      <v-divider></v-divider>

      <!-- Sidebar Items -->
      <v-list dense nav>
        <v-list-item
          v-for="(item, idx) in items"
          :to="item.route"
          :key="idx"
          class="sidebar-link"
          link
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <!-- Version -->
      <div class="version-wrapper">
        <div class="body-2">{{ version.main }}</div>
        <div class="caption">{{ version.build }}</div>
      </div>

    </v-navigation-drawer>
  </div>
</template>

<script>
export default {
  name: 'Sidebar',
  data: () => ({
    title: 'Image Labeller',
    subtitle: 'for KHU Capstone Design 1',
    items: [
      { title: 'Main', icon: 'mdi-view-dashboard', route: '/main' },
      { title: 'Settings', icon: 'mdi-cog-outline', route: '/settings' }
    ],
    version: {
      main: 'v0.7.3-alpha',
      build: 'build-2004080227'
    }
  })
}
</script>

<style lang="scss" scoped>
.sidebar {
  .nonselectable-text {
    user-select: none;
  }
  .sidebar-link {
    -webkit-app-region: no-drag;
  }
  .version-wrapper {
    position: absolute;
    bottom: 10px;
    right: 10px;
    color: #aaa;
    text-align: right;
  }
}
</style>
