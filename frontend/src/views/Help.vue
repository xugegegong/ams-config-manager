<template>
  <div>
    <div class="page-header">
      <h2>📖 参考说明</h2>
      <p class="desc">功能说明与操作指南</p>
    </div>

    <el-card>
      <div class="help-content">
        <h3>系统概述</h3>
        <p>本系统用于替代原 HldAssistant 桌面程序的配置管理功能，提供 Web 化的操作界面。</p>

        <h3>一、数据库操作</h3>
        <p>在<strong>数据库操作</strong>页面，输入 MySQL 数据库的连接信息（IP、端口、用户名、密码、数据库名），点击"连接数据库"按钮测试连接是否正常。</p>
        <ul>
          <li>连接成功后底部状态条会显示绿色"数据库已连接"</li>
          <li>目标数据库为船舶端的数据存储库</li>
        </ul>

        <h3>二、机舱设备配置</h3>
        <p>在<strong>机舱设备</strong>页面，按照以下步骤操作：</p>
        <ol>
          <li><strong>选择船舶</strong> — 从下拉框选择当前操作的船舶</li>
          <li><strong>选择网关</strong> — 选择 SailingData（航行数据）或 EngineData（机舱数据）</li>
          <li><strong>选择/新建 Modbus 客户端</strong> — 选择已有的 AMS 客户端或点"新增客户端"创建</li>
          <li><strong>配置通讯参数</strong> — 设置波特率、数据位、校验位、从站ID、功能码等</li>
          <li><strong>管理工况点</strong> — 可通过"Excel导入"批量导入，也可手动增删改</li>
          <li><strong>生成配置</strong> — 点击红色"生成配置"按钮，生成 JSON + TXT 配置文件</li>
        </ol>

        <h3>三、AMS Excel 导入（核心功能）</h3>
        <p>不同 AMS 厂商提供的 Excel 格式各不相同，系统支持灵活的列映射配置：</p>
        <ol>
          <li><strong>上传文件</strong> — 拖拽或选择 AMS 厂商的 Excel 文件</li>
          <li><strong>选择或创建模板</strong> — 如果已有该厂商的导入模板，直接选择；否则新建映射</li>
          <li><strong>列映射</strong> — 将 Excel 的列与系统字段一一对应（名称、Modbus地址、信号类型等）</li>
          <li><strong>保存模板</strong> — 同系列船下次可直接复用</li>
          <li><strong>版本比对</strong> — 系统自动对比新旧版本，列出新增/删除/修改的工况点</li>
          <li><strong>审批入库</strong> — 确认无误后一键导入</li>
        </ol>

        <h3>四、配置入库（cfg2DB）</h3>
        <p>在<strong>配置入库</strong>页面，选择目标数据库并点击对应客户端的"配置入库"按钮，系统将配置数据写入数据库的 <code>channelsdataprotocol</code> 表中。</p>

        <h3>五、版本管理</h3>
        <p>每次导入新版本 Excel，系统自动与前一个版本比对，生成变更报告：</p>
        <ul>
          <li><span style="color: #52c41a;">🟢 新增</span> — 新版本中增加的工况点</li>
          <li><span style="color: #ff4d4f;">🔴 删除</span> — 新版本中移除的工况点</li>
          <li><span style="color: #faad14;">🟡 修改</span> — 名称、地址、类型等发生变化的工况点</li>
        </ul>
        <p>支持逐条审批或一键全部接受/拒绝。</p>

        <h3>六、注意事项</h3>
        <ul>
          <li>首次使用请先在登录页使用 admin/admin123 初始化管理员账号</li>
          <li>数据库连接信息保存后仅供当前会话使用</li>
          <li>Excel 文件仅用于导入，不会永久保存</li>
          <li>建议每次导入新版本前先备份当前配置</li>
        </ul>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.help-content {
  line-height: 1.8;
  color: #d0d0e0;
}
.help-content h3 {
  color: #4a9eff;
  margin: 24px 0 12px;
  font-size: 16px;
}
.help-content h3:first-child {
  margin-top: 0;
}
.help-content p {
  margin: 8px 0;
}
.help-content ol, .help-content ul {
  padding-left: 24px;
}
.help-content li {
  margin: 4px 0;
}
.help-content code {
  background: #2a2a48;
  padding: 2px 8px;
  border-radius: 3px;
  font-size: 13px;
  color: #4a9eff;
}
</style>
