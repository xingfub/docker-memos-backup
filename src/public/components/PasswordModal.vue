<template>
  <div class="modal-overlay" v-if="show">
    <div class="modal-container">
      <div class="modal-header">
        <h3 class="modal-title">🔐 请输入密码</h3>
      </div>
      <div class="modal-body">
        <div class="form-group">
          <input 
            type="password" 
            v-model="password" 
            class="form-input" 
            placeholder="请输入访问密码"
            @keyup.enter="handleSubmit"
            autofocus
          />
        </div>
        <div v-if="error" class="error-message">{{ error }}</div>
      </div>
      <div class="modal-footer">
        <button class="btn btn-primary" @click="handleSubmit">确认</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PasswordModal',
  props: {
    show: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      password: '',
      error: ''
    }
  },
  methods: {
    async handleSubmit() {
      if (!this.password.trim()) {
        this.error = '密码不能为空';
        return;
      }
      try {
        const res = await axios.post('/api/check-password', { password: this.password });
        if (res.data.code === 200) {
          this.error = '';
          this.password = '';
          this.$emit('success');
        } else {
          this.error = res.data.message;
        }
      } catch (e) {
        this.error = '验证失败，请重试';
      }
    }
  },
  watch: {
    show(newVal) {
      if (newVal) {
        this.password = '';
        this.error = '';
      }
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-container {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 400px;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  padding: 20px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.modal-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.modal-body {
  padding: 24px;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
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

.error-message {
  color: #ef4444;
  font-size: 12px;
  margin-top: 8px;
}

.modal-footer {
  padding: 16px 24px;
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
  text-align: right;
}

.btn {
  padding: 10px 24px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}
</style>