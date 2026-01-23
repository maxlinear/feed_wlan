#
# Openwrt Makefile for Shared Headers
#
#
#

#### Includes ###################################
include $(TOPDIR)/rules.mk
include $(INCLUDE_DIR)/kernel.mk

PKG_NAME:=iwlwav_shared_header
PKG_REV:=0c3534da0649f2006b22592ff3a2190594743a35
PKG_VERSION:=1.0
PKG_RELEASE:=$(PKG_REV)
PKG_SOURCE:=$(PKG_NAME).tar.bz2
PKG_PROJECT:=maxlinear
PKG_SOURCE_NAME:=shared_header.git
CONFIG_UGW_PKG_SOURCE_URL:=https://github.com
PKG_SOURCE_URL:=$(CONFIG_UGW_PKG_SOURCE_URL)/$(PKG_PROJECT)/$(PKG_SOURCE_NAME)
PKG_SOURCE_VERSION:=r1516+a+24
PKG_SOURCE_PROTO:=git
PKG_MIRROR_HASH:=fa72822d4127d679a2be0d14d97f7bc736df32a71e7bb70023ec0c9f24ed9d57

PKG_MAINTAINER:=MaxLinear
PKG_LICENSE:=MaxLinear
PKG_LICENSE_FILES:=LICENSE

PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)

include $(INCLUDE_DIR)/package.mk
-include $(INCLUDE_DIR)/package-version-override.mk

define Package/iwlwav_shared_header
	SECTION:=utils
	CATEGORY:=MaxLinear
	TITLE:=wave SW shared headers
	URL:=https://www.maxlinear.com
	MENU:=1
	VARIANT:=release
	VERSION:=$(PKG_VERSION)
endef

define Package/iwlwav_shared_header/description
	MaxLinear wave SW shared headers
endef

define Build/Prepare
	$(call Build/Prepare/Default)
endef

define Build/Compile
	# No actual compilation needed
	echo "Nothing to compile"
endef

define Package/iwlwav_shared_header/install
	# No actual installation needed
	echo "Nothing to install"
endef

$(eval $(call BuildPackage,iwlwav_shared_header))
