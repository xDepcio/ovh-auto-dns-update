# ovh-auto-dns-update

## Example Usage
### Manual Update
Run scriupt with following options:

```bash
ovh-auto-dns-update update --domain '<example.com>' --subomain '<subdomain1>' --subdomain '<subdomain2>' --application-key '<OVH app key>' --application-secret '<OVH app secret>' --consumer-key '<OVH consumer key>'
```

`ovh-auto-dns-update` is bundled Python script that updates your OVH DNS records automatically based on change in your public IP. Executable needs to be inside `PATH` or you need to provide full path to the script.

### Automatic Update
Easiest way to automate this is to use `cron` job. Add and moify following line to your `crontab -e`, to run script every day at 1AM:

```txt
0 1 * * * ovh-auto-dns-update update --domain '<example.com>' --subomain '<subdomain1>' --subdomain '<subdomain2>' --application-key '<OVH app key>' --application-secret '<OVH app secret>' --consumer-key '<OVH consumer key>'
```
