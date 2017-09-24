#!/usr/bin/env python
# -*- coding: utf-8 -*-


from brew.utilities.temperature import mash_infusion
from brew.utilities.temperature import strike_temp


def main():

    print("Enzymatic rests schedule")

    liquor_to_grist_ratio = 1.5  # qt:lbs
    grain_weight = 8.0  # lbs
    water_volume = grain_weight * liquor_to_grist_ratio  # qt

    print("")
    print("Starting with {} lbs of grain".format(grain_weight))

    target_temp = 110
    initial_temp = 70  # grain temperature without water
    sk_temp = strike_temp(target_temp, initial_temp,
                          liquor_to_grist_ratio=liquor_to_grist_ratio)

    print("")
    print("Bring {} qts of water to {} degF before adding grains".format(
        water_volume, round(sk_temp, 1)))  # noqa
    print("Your temperature should then reach {} degF".format(target_temp))
    print("Keep your temperature here for 20 minutes")

    initial_temp = sk_temp
    target_temp = 140
    infusion_temp = 210

    infusion_volume = mash_infusion(target_temp, initial_temp,
                                    grain_weight, water_volume,
                                    infusion_temp=infusion_temp)

    print("")
    print("Add {} qts of {} degF water".format(round(infusion_volume, 1), infusion_temp))  # noqa
    print("Your temperature should then reach {} degF".format(target_temp))
    print("Keep your temperature here for 40 minutes")

    initial_temp = target_temp
    target_temp = 158
    infusion_temp = 210
    water_volume += infusion_volume

    infusion_volume = mash_infusion(target_temp, initial_temp,
                                    grain_weight, water_volume,
                                    infusion_temp=infusion_temp)

    print("")
    print("Add {} qts of {} degF water".format(round(infusion_volume, 1), infusion_temp))  # noqa
    print("Your temperature should then reach {} degF".format(target_temp))
    print("Keep your temperature here for 20 minutes")
    print("")

    water_volume += infusion_volume
    print("You should now have {} qts of water".format(round(water_volume, 1)))
    print("Now remove the grains and continue with brewing")


if __name__ == "__main__":
    main()
