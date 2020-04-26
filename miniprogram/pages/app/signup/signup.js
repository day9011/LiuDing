// pages/app/signup/signup.js
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
    grade_options: {
      array: ['一年级', '二年级'],
      objectArray: [
        {
          id: 0,
          name: '一年级'
        },
        {
          id: 1,
          name: '二年级'
        }
      ],
      grade_index: 0,
    },
    subject_options: {
      array: ['数学', '英语'],
      objectArray: [
        {
          id: 0,
          name: '数学'
        },
        {
          id: 1,
          name: '英语'
        }
      ],
      subject_index: 0,
    },
    class_times:  {
      array: ['7:00~8:00', '9:00~10:00'],
      objectArray: [
        {
          id: 0,
          name: '7:00~8:00'
        },
        {
          id: 1,
          name: '9:00~10:00'
        }
      ],
      time_index: 0,
    },
    fee: "100rmb",
    items: [
      {'value': '1', 'name': '上学期', checked: 'true'},
      {'value': '2', 'name': '寒假'},
      {'value': '3', 'name': '下学期'},
      {'value': '4', 'name': '暑期'}
    ],
    user_name: "",
    user_grade: "",
    user_parent_name: "",
    user_parent_phone: ""
  },

  /**
   * 组件的方法列表
   */
  methods: {
    GradeChange: function (e) {
      console.log('picker发送选择改变，携带值为', e.detail.value)
      this.setData({
        grade_index: e.detail.value
      })
    },
    SubjectChange: function (e) {
      console.log('picker发送选择改变，携带值为', e.detail.value)
      this.setData({
        subject_index: e.detail.value
      })
    },
    ClassTimeChange: function (e) {
      console.log('picker发送选择改变，携带值为', e.detail.value)
      this.setData({
        time_index: e.detail.value
      })
    },
    NameInput: function(e) {
      this.setData({
        user_name: e.detail.value
      })
    },
    GradeInput: function(e) {
      this.setData({
        user_grade: e.detail.value
      })
    },
    ParentInput: function(e) {
      this.setData({
        user_parent_name: e.detail.value
      })
    },
    PhoneInput: function(e) {
      this.setData({
        user_parent_phone: e.detail.value
      })
    },
    Submit: function(e) {
      console.log(this.data);
    }
  }
  
})
