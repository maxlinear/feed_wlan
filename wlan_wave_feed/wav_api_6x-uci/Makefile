#
# Openwrt Makefile for wav_api-uci
#

#### Includes ###################################
include $(TOPDIR)/rules.mk

#### Package Info ############################### 
PKG_NAME:=wav_api_6x-uci
PKG_REV:=a03109b72409a8350a673e70450b6cf4a33af2a1
PKG_VERSION:=1.0.0.1
PKG_RELEASE:=$(PKG_REV)
PKG_BASE_NAME:=$(PKG_NAME)
PKG_SOURCE:=$(PKG_BASE_NAME)-$(PKG_VERSION)-$(PKG_REV).tar.bz2
PKG_PROJECT:=mxl-oss/wifi
PKG_SOURCE_NAME:=wav_api.git
CONFIG_UGW_PKG_SOURCE_URL:=ssh://git@git.maxlinear.com
PKG_SOURCE_URL:=$(CONFIG_UGW_PKG_SOURCE_URL)/$(PKG_PROJECT)/$(PKG_SOURCE_NAME)
PKG_SOURCE_VERSION:=r597+a+41
PKG_SOURCE_SUBDIR:=$(PKG_BASE_NAME)-$(PKG_VERSION)
PKG_SOURCE_PROTO:=git
PKG_MIRROR_HASH:=ca20e4648573c3974d73d0a234037cd2e0271337843ebdc7c22adc41e5d52868
#PKG_MD5SUM:=40b89c61036add0c2dd1fc10767d3b5f

PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(BUILD_VARIANT)/$(PKG_BASE_NAME)-$(PKG_VERSION)
PKG_DEFAULT_CUSTOM_SOURCE_DIR:=$(shell pwd)

PKG_MAINTAINER:=MaxLinear
PKG_LICENSE:=MaxLinear
PKG_LICENSE_FILES:=LICENSE

PKG_VARIANT_DWPAL_SUFFIX=
ifeq ($(BUILD_VARIANT),debug)
  PKG_VARIANT_DWPAL_SUFFIX=-debug
endif
ifeq ($(BUILD_VARIANT),osp-debug)
  PKG_VARIANT_DWPAL_SUFFIX=-osp-debug
endif
ifeq ($(BUILD_VARIANT),osp)
  PKG_VARIANT_DWPAL_SUFFIX=-osp
endif

PKG_VARIANT_SWPAL_SUFFIX=
ifeq ($(BUILD_VARIANT), $(filter debug osp-debug, $(BUILD_VARIANT)))
  PKG_VARIANT_SWPAL_SUFFIX=-debug
endif

PKG_BUILD_DEPENDS:=dwpal_6x-uci$(PKG_VARIANT_DWPAL_SUFFIX) swpal_6x-uci$(PKG_VARIANT_SWPAL_SUFFIX)

export OPT_VENDOR_PATH=$(findstring intel,$(CONFIG_TARGET_BOARD))
ifeq ($(OPT_VENDOR_PATH),)
export OPT_VENDOR_PATH=lantiq
endif

include $(INCLUDE_DIR)/package.mk
-include $(INCLUDE_DIR)/package-version-override.mk
define Package/$(PKG_NAME)
  SECTION:=net
  CATEGORY:=MaxLinear
  SUBMENU:=UGW Software
  TITLE:=WAV-API Library
  URL:=http://www.maxlinear.com
  MAINTAINER:=MaxLinear Inc
  DEPENDS:= +libnl +librt +libsafec3 +libncurses +dwpal_6x-uci +swpal_6x-uci
  MENU:=1
  VARIANT:=release
endef

define Package/$(PKG_NAME)/description
	WAV-API: WAV API Layer. Includes: band steering lite application.
endef

define Package/$(PKG_NAME)-debug
$(call Package/$(PKG_NAME))
VARIANT:=debug
DEPENDS:= +libnl +librt +libsafec3 +libncurses +dwpal_6x-uci-debug +swpal_6x-uci-debug
TITLE += with debug information
endef

define Package/$(PKG_NAME)-debug/description
$(call Package/$(PKG_NAME)/description) with debug information
endef

define Package/$(PKG_NAME)-osp
$(call Package/$(PKG_NAME))
TITLE += with opensource packages
VARIANT:=osp
DEPENDS:=+libnl +librt +libsafec3 +libncurses +dwpal_6x-uci-osp +swpal_6x-uci
endef

define Package/$(PKG_NAME)-osp/description
$(call Package/$(PKG_NAME)/description) with opensource packages
endef

define Package/$(PKG_NAME)-osp-debug
$(call Package/$(PKG_NAME))
TITLE += with opensource packages and debug information
VARIANT:=osp-debug
DEPENDS:=+libnl +librt +libsafec3 +libncurses +dwpal_6x-uci-osp-debug +swpal_6x-uci-debug
endef

define Package/$(PKG_NAME)-osp-debug/description
$(call Package/$(PKG_NAME)/description) with opensource packages and debug information
endef

IFX_CFLAGS += -I$(STAGING_DIR)/usr/include/
TARGET_CFLAGS += -DCONFIG_RPCD -DHAVE_C99=1
TARGET_LDFLAGS += -L$(STAGING_DIR)/usr/lib -lsafec-3.3
IFX_CFLAGS += -fstack-protector-strong -O2 -D_FORTIFY_SOURCE=2 -Wformat -Wformat-security -Werror=format-security -Wall -fPIC -Wl,-strip-debug
IFX_LDFLAGS += -Wl,-z,noexecstack -Wl,-z,now -Wl,-z,relro

ifeq ($(BUILD_VARIANT), $(filter debug osp-debug, $(BUILD_VARIANT)))
TARGET_CFLAGS += -DCONFIG_WAVE_DEBUG
endif

# To ipkg / Rootfs
define Package/$(PKG_NAME)/install
	$(INSTALL_DIR) $(1)/usr/sbin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/band_steering $(1)/usr/sbin
	chmod 555 $(1)/usr/sbin/band_steering
endef

Package/$(PKG_NAME)-debug/install = $(Package/$(PKG_NAME)/install)
Package/$(PKG_NAME)-osp/install = $(Package/$(PKG_NAME)/install)
Package/$(PKG_NAME)-osp-debug/install = $(Package/$(PKG_NAME)/install)

define Build/Clean
	if [ -d $(PKG_BUILD_DIR) ]; then $(MAKE) -C $(PKG_BUILD_DIR) clean; \
	$(RM) -r $(PKG_BUILD_DIR)/ipkg-$(BOARD); fi
endef

$(eval $(call BuildPackage,$(PKG_NAME)))
$(eval $(call BuildPackage,$(PKG_NAME)-debug))
$(eval $(call BuildPackage,$(PKG_NAME)-osp))
$(eval $(call BuildPackage,$(PKG_NAME)-osp-debug))
