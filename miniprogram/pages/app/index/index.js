// pages/app/index/index.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {

  },

  /**
   * 组件的初始数据
   */
  data: {
    currentTab: 11
  },

  /**
   * 组件的方法列表
   */
  methods: {
    switchTab(e) {
      console.log(e)
      let tab = e.currentTarget.id
      if (tab === 'tabmath') {
        this.setData({ currentTab: 11 })
      } else if (tab === 'tabarticle') {
        this.setData({ currentTab: 12 })
      } else if (tab === 'tabenglish') {
        this.setData({ currentTab: 13 })
      } else if (tab === 'tabstudent') {
        this.setData({ currentTab: 14 })
      }
    }
  }
})
