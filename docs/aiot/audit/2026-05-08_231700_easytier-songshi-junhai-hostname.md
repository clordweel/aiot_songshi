## 2026-05-08 23:17:00 — EasyTier 配置：songshi 网络与 junhai 公共节点

- 时间：2026-05-08 23:17:00 UTC（现场以服务器 journal 为准；本地操作为同日）
- 环境：VM `10.0.0.40`（`aiot-songshi-frappe`），`/opt/easytier/config/default.conf`，systemd `easytier@default`
- 类型：deploy
- 摘要：将虚拟网标识与密钥更新为团队约定值；公共 peer 设为 `tcp://easytier.junhai.work:11010`；`hostname` 设为 `aiot_songshi`；`systemctl restart easytier@default`；`easytier-cli node` 显示虚拟 IP 与主机名正确，`easytier-cli peer` 显示已与公共服务器建立连接。
- 结果：ok
- 审批（可选）：
