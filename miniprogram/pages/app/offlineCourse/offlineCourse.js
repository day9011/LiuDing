// pages/app/offlineCourse/offlineCourse.js
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

  },

  /**
   * 组件的方法列表
   */
  methods: {
    signup: function() {
      wx.navigateTo({
        url: '/pages/app/signup/signup',
      })
    }
  }
})
