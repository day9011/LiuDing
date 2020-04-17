
  Component({
    data: {
      selected: 0,
      color: "#7A7E83",
      selectedColor: "#3cc51f",
      position: "top",
      list:
      [
        {
          "pagePath": "/pages/index/subindex/math/index",
          "text": "奥数难题"
        },
        {
          "pagePath": "/pages/index/subindex/composition/index",
          "text": "优秀作文"
        },
        {
          "pagePath": "/pages/index/subindex/english/index",
          "text": "英语天地"
        },
        {
          "pagePath": "/pages/index/subindex/good/index",
          "text": "优秀学员"
        }
      ]
    },
    attached() {
    },
    methods: {
      switchTab(e) {
        const data = e.currentTarget.dataset
        const url = data.path
        wx.switchTab({
          url: url,
        })
      }
    }
  })