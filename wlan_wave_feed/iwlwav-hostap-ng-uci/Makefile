#
# Openwrt Makefile for hostapd
#
# Simplify mode 1.0
#
#

#### Includes ###################################
include $(TOPDIR)/rules.mk
include $(INCLUDE_DIR)/kernel.mk

PKG_NAME:=iwlwav-hostap-ng-uci
PKG_REV:=95ad71157e3095c52d5212855ca232832b1b5085
PKG_VERSION:=2.10
PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.bz2
PKG_PROJECT:=maxlinear
PKG_SOURCE_NAME:=iwlwav-hostap-ng.git
CONFIG_UGW_PKG_SOURCE_URL:=https://github.com
PKG_SOURCE_URL:=https://git.w1.fi/hostap.git
PKG_SOURCE_VERSION:=95ad71157e3095c52d5212855ca232832b1b5085
PKG_SOURCE_PROTO:=git
PKG_MIRROR_HASH:=a34188f8b9df9f8cf54300a2c579f451d717ff7adaf4e40bd19a7f5104ed3401
ifeq ($(BUILD_VARIANT),debug)
PKG_CONFIG_DEPENDS:=CONFIG_WIRELESS_STA-debug CONFIG_LIBCURL_OPENSSL CONFIG_LIBCURL_SSH2 CONFIG_LIBCURL_VERBOSE CONFIG_PACKAGE_libjson-c
else
PKG_CONFIG_DEPENDS:=CONFIG_WIRELESS_STA CONFIG_LIBCURL_OPENSSL CONFIG_LIBCURL_SSH2 CONFIG_LIBCURL_VERBOSE CONFIG_PACKAGE_libjson-c
endif
ifeq ($(CONFIG_BUILD_SDK),"prplos")
BUILD_SDK:="updk-"
else
BUILD_SDK:=""
endif
ifeq ($(CONFIG_MXL_WLAN_OSS_BUILD),y)
BUILD_TYPE:="oss-"
else
BUILD_TYPE:=""
endif

PKG_BUILD_DIR:=$(BUILD_DIR)/iwlwav-hostap-ng-uci-$(BUILD_VARIANT)/iwlwav-hostap-ng-uci-$(PKG_VERSION)
PKG_BUILD_DEPENDS:=openssl libnl safec3 iwlwav-hostap-ng-uci/host
#PKG_BUILD_DEPENDS += iwlwav-driver-uci

PKG_LICENSE:=BSD
PKG_LICENSE_FILES:=README

PATCH_DIR:=./patches_external

# The commented variables below are used internally by <os_set_release_mode.py> script (located at
# the root directory of this repository). They are commented on purpose to avoid conflicting with
# other tools. DO NOT REMOVE THOSE LINES. OS_REPO_URL is the clone URL of the open-source repository
# and OS_FORK_REF is the reference (a tag or a commit) where MaxLinear has forked from the open-source
# repository.

# OS_REPO_URL:=git://w1.fi/hostap.git
# OS_FORK_REF:=hostap_2_10

include $(INCLUDE_DIR)/package.mk
-include $(INCLUDE_DIR)/package-version-override.mk

define Package/iwlwav-hostap-ng-uci
  SECTION:=net
  CATEGORY:=Network
  TITLE:=hostapd for Wave
  DEPENDS:=+libopenssl +librt +libnl +libsafec3 +libubus +libubox +libcurl +libjson-c
  MENU:=1
  PROVIDES:=iwlwav-hostap
  VARIANT:=release
endef

define Package/iwlwav-hostap-ng-uci/description
  IEEE 802.11 AP, IEEE 802.1X/WPA/WPA2/EAP/RADIUS Authenticator
endef
define Package/iwlwav-hostap-ng-uci/config
$(call Package/iwlwav-hostap-ng-uci/override_version)
$(call Package/iwlwav-hostap-ng-uci/override_source_path)
    config WIRELESS_STA
      depends on PACKAGE_iwlwav-hostap-ng-uci
      bool 'Linux WPA/WPA2/IEEE 802.1X Supplicant support'
      help
          Linux WPA/WPA2/IEEE 802.1X Supplicant
    config WIRELESS_AFC
      depends on PACKAGE_$(PKG_NAME)
      bool 'WLAN AFC feature support'
      default y
      help
          WiFi Automated Frequency Coordination to enable using standard power modes in the 6GHz band
endef

define Package/iwlwav-hostap-ng-uci-debug
$(call Package/iwlwav-hostap-ng-uci)
VARIANT:=debug
TITLE += with debug information
endef

define Package/iwlwav-hostap-ng-uci-debug/description
$(call Package/iwlwav-hostap-ng-uci/description) with debug information
endef

define Package/iwlwav-hostap-ng-uci-debug/config
$(call Package/iwlwav-hostap-ng-uci-debug/override_version)
$(call Package/iwlwav-hostap-ng-uci-debug/override_source_path)
    config WIRELESS_STA-debug
      depends on PACKAGE_iwlwav-hostap-ng-uci-debug
      bool 'Linux WPA/WPA2/IEEE 802.1X Supplicant support with debug'
      help
          Linux WPA/WPA2/IEEE 802.1X Supplicant with Debug information
    config WIRELESS_AFC-debug
      depends on PACKAGE_$(PKG_NAME)-debug
      bool 'WLAN AFC feature support with debug'
      default y
      help
          WiFi Automated Frequency Coordination to enable using standard power modes in the 6GHz band
endef
LIBRT_DIR:=$(TOOLCHAIN_DIR)

USR_INC_DIR:=$(wildcard $(STAGING_DIR)/usr/include)

IFX_CFLAGS += -I$(USR_INC_DIR)/include -DHAVE_C99=1
IFX_LDFLAGS += -L$(STAGING_DIR)/usr/lib -lnl-3 -L$(LIBRT_DIR)/lib -lrt -lsafec-3.3 -lcurl -ljson-c
IFX_CFLAGS += -fstack-protector-strong -O2 -D_FORTIFY_SOURCE=2 -Wformat -Wformat-security -Werror=format-security -Wall -Wtype-limits -fPIE -Wl,-strip-debug
IFX_LDFLAGS_AFC = $(IFX_LDFLAGS)
IFX_LDFLAGS_AFC += -Wl,-z,noexecstack -Wl,-z,now -Wl,-z,relro -no-pie
IFX_LDFLAGS += -Wl,-z,noexecstack -Wl,-z,now -Wl,-z,relro -pie
ifeq ($(BUILD_VARIANT),debug)
IFX_CFLAGS += -DCONFIG_WAVE_DEBUG #-DCONFIG_NO_HOSTAPD_LOGGER
CONFIG_SUFFIX =-debug
endif

include $(INCLUDE_DIR)/host-build.mk

# Depend on host-side elfutils
HOST_BUILD_DEPENDS:=elfutils
HOST_LDFLAGS += -lelf -ldw -lz -lpthread
HOST_MAKE_PATH := hostapd

define Host/Compile
	$(MAKE) -C $(HOST_BUILD_DIR)/hostapd \
	HOSTCC="$(HOSTCC)" \
	HOST_CFLAGS="$(HOST_CFLAGS)" \
	HOST_LDFLAGS="$(HOST_LDFLAGS)" \
	CONFIG_VENDOR_MXL=y \
	mxl_hostapd_metadata
endef

define Host/Install
	$(INSTALL_DIR) $(STAGING_DIR_HOSTPKG)/bin
	$(INSTALL_BIN) $(HOST_BUILD_DIR)/hostapd/mxl_hostapd_metadata \
		$(STAGING_DIR_HOSTPKG)/bin/
endef

#TODO: Add check when hostap-ng's headers will be aligned with the rest
#RELATIVE_NLV_PKG_HEADER_PATH:=src/common/vendor_cmds_copy.h
#RELATIVE_NL_PKG_HEADER_PATH:=src/drivers/nl80211_copy.h
#../iwlwav-driver-uci/files/check_shared_headers.sh $(PKG_NAME) $(PKG_VERSION) $(BUILD_DIR) $(BUILD_VARIANT) $(RELATIVE_NLV_PKG_HEADER_PATH) $(RELATIVE_NL_PKG_HEADER_PATH)

define Build/Compile
	$(MAKE) -C $(PKG_BUILD_DIR)/src clean
	$(CP) ./files/hostapd/defconfig-$(BUILD_SDK)$(BUILD_TYPE)$(BUILD_VARIANT) $(PKG_BUILD_DIR)/hostapd/.config
	$(MAKE) $(TARGET_CONFIGURE_OPTS) -C $(PKG_BUILD_DIR)/hostapd \
		EXTRA_CFLAGS="$(IFX_CFLAGS)" LDFLAGS="$(IFX_LDFLAGS)"
	$(STAGING_DIR_HOSTPKG)/bin/mxl_hostapd_metadata $(PKG_BUILD_DIR)/hostapd/hostapd $(PKG_BUILD_DIR)/hostapd/hostapd_metadata.txt
	$(if $(or $(CONFIG_WIRELESS_STA),$(CONFIG_WIRELESS_STA-debug)), \
		$(MAKE) -C $(PKG_BUILD_DIR)/src clean; \
		$(CP) ./files/wpa_supplicant/defconfig-$(BUILD_VARIANT) $(PKG_BUILD_DIR)/wpa_supplicant/.config; \
		$(MAKE) $(TARGET_CONFIGURE_OPTS) -C $(PKG_BUILD_DIR)/wpa_supplicant \
		    EXTRA_CFLAGS="$(IFX_CFLAGS)" LDFLAGS="$(IFX_LDFLAGS)" \
	)
	$(MAKE) -C $(PKG_BUILD_DIR)/src clean; \
	$(MAKE) $(TARGET_CONFIGURE_OPTS) -C $(PKG_BUILD_DIR)/afc \
		EXTRA_CFLAGS="$(IFX_CFLAGS)" LDFLAGS="$(IFX_LDFLAGS_AFC)"
endef

define Build/InstallDev
	$(INSTALL_DIR) $(1)/usr/include
	$(CP) $(PKG_BUILD_DIR)/src/common/wpa_ctrl.h $(1)/usr/include
endef

define Package/iwlwav-hostap-ng-uci/install
	$(INSTALL_DIR) $(1)/usr/sbin
	$(INSTALL_DIR) -p $(1)/etc
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/hostapd/hostapd $(1)/usr/sbin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/hostapd/hostapd_cli $(1)/usr/sbin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/hostapd/hostapd.eap_user $(1)/usr/sbin
	$(INSTALL_BIN) ./files/hostapd_conf/* $(1)/etc
	$(if $(or $(CONFIG_WIRELESS_STA),$(CONFIG_WIRELESS_STA-debug)), \
		$(INSTALL_BIN) $(PKG_BUILD_DIR)/wpa_supplicant/wpa_supplicant $(1)/usr/sbin; \
		$(INSTALL_BIN) $(PKG_BUILD_DIR)/wpa_supplicant/wpa_cli $(1)/usr/sbin; \
		$(INSTALL_BIN) $(PKG_BUILD_DIR)/wpa_supplicant/wpa_passphrase $(1)/usr/sbin \
	)
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/afc/afcd $(1)/usr/sbin
	$(INSTALL_DIR) $(1)/etc/init.d/
	$(if $(filter $(CONFIG_BUILD_SDK),"prplos"), \
		$(INSTALL_BIN) ./files/afc_initd_prpl $(1)/etc/init.d/afc_initd; \
	)
	$(if $(filter $(CONFIG_BUILD_SDK),"ugw"), \
		$(INSTALL_BIN) ./files/afc_initd $(1)/etc/init.d/afc_initd; \
	)
	echo -e "iwlwav_hostap_hash=\"$(PKG_REV)\"\niwlwav_hostap_tag=\"$(PKG_REV)\"" > $(1)/etc/iwlwav_hostap.ver
endef

define Package/iwlwav-hostap-ng-uci-debug/install
	$(call Package/iwlwav-hostap-ng-uci/install,$(1))
	$(INSTALL_DATA) $(PKG_BUILD_DIR)/hostapd/hostapd_metadata.txt $(1)/etc/hostapd_metadata.txt
endef

$(eval $(call HostBuild))
$(eval $(call BuildPackage,iwlwav-hostap-ng-uci))
$(eval $(call BuildPackage,iwlwav-hostap-ng-uci-debug))
