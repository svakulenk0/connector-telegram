# opsdroid connector telegram

A connector for [opsdroid](https://github.com/opsdroid/opsdroid) to send messages using [Telegram](https://telegram.org/).

## Requirements

You need to [register a bot](https://core.telegram.org/bots) on Telegram and get an api token for it.

## Configuration

```yaml
connectors:
  - name: telegram
    # required
    token: "123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZ-ZYXWVUT"
    # optional
    whitelisted_users:
      - user1
      - user2
```

## License

GNU General Public License Version 3 (GPLv3)
