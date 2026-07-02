<template>
  <div class="settings-tab">
    <div class="settings-card">
      <h4 class="settings-title">🔐 密码设置</h4>

      <div class="form-group">
        <label>新密码</label>
        <input 
          v-model="newPassword" 
          type="password" 
          class="form-input" 
          placeholder="请输入新密码"
        />
      </div>

      <div class="form-group">
        <label>确认密码</label>
        <input 
          v-model="confirmPassword" 
          type="password" 
          class="form-input" 
          placeholder="请确认密码"
        />
      </div>

      <div v-if="message" :class="['message', { success: success, error: !success }]">
        {{ message }}
      </div>

      <div class="form-actions">
        <button class="btn btn-primary" @click="setPassword">
          <span class="btn-icon">✅</span>
          设置密码
        </button>
        <button class="btn btn-danger" @click="clearPassword">
          <span class="btn-icon">🗑️</span>
          清除密码
        </button>
      </div>
    </div>

    <div class="info-card">
      <h5 class="info-title">ℹ️ 安全提示</h5>
      <ul class="info-list">
        <li>设置密码后，每次访问页面都需要验证</li>
        <li>请设置一个安全且容易记住的密码</li>
        <li>清除密码后，任何人都可以直接访问</li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SettingsTab',
  data() {
    return {
      newPassword: '',
      confirmPassword: '',
      message: '',
      success: false
    }
  },
  methods: {
    async setPassword() {
      if (!this.newPassword) {
        return this.showMessage('密码不能为空', false)
      }
      if (this.newPassword !== this.confirmPassword) {
        return this.showMessage('两次密码不一致', false)
      }

      try {
        const res = await axios.post('/api/set-password', { password: this.newPassword })
        this.showMessage(res.data.message, res.data.code === 200)
        this.newPassword = ''
        this.confirmPassword = ''
      } catch (e) {
        this.showMessage('设置失败', false)
      }
    },
    async clearPassword() {
      if (!confirm('确定要清除密码吗？清除后任何人都可以直接访问此页面。')) {
        return
      }

      try {
        const res = await axios.post('/api/clear-password')
        this.showMessage(res.data.message, res.data.code === 200)
      } catch (e) {
        this.showMessage('清除失败', false)
      }
    },
    showMessage(msg, isSuccess) {
      this.message = msg
      this.success = isSuccess
      setTimeout(() => {
        this.message = ''
      }, 3000)
    }
  }
}
</script>

<style scoped>
.settings-tab {
  padding: 20px;
}

.settings-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  margin-bottom: 20px;
}

.settings-title {
  margin: 0 0 20px 0;
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: #4b5563;
  margin-bottom: 6px;
}

.form-input {
  width: 100%;
  padding: 10px 14px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.3s;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-input::placeholder {
  color: #9ca3af;
}

.message {
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 13px;
  margin-bottom: 16px;
}

.message.success {
  background: #dcfce7;
  color: #166534;
}

.message.error {
  background: #fee2e2;
  color: #991b1b;
}

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  padding-top: 16px;
  border-top: 1px solid #f3f4f6;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-danger {
  background: #fee2e2;
  color: #dc2626;
}

.btn-danger:hover {
  background: #fecaca;
  transform: translateY(-1px);
}

.btn-icon {
  font-size: 16px;
}

.info-card {
  background: #eff6ff;
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #bfdbfe;
}

.info-title {
  margin: 0 0 12px 0;
  font-size: 14px;
  font-weight: 600;
  color: #1e40af;
}

.info-list {
  margin: 0;
  padding-left: 20px;
}

.info-list li {
  font-size: 13px;
  color: #3b82f6;
  margin-bottom: 6px;
}

.info-list li:last-child {
  margin-bottom: 0;
}
</style>