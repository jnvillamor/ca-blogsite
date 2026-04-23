import { Button } from '@/common/components/ui/button'
import Link from 'next/link'
import React from 'react'

const ProfileActionButtons = () => {
  return (
    <div className="flex flex-col sm:flex-row gap-3 mb-8">
      <Button variant='outline' asChild className='gap-2'>
        <Link href='/blogs'>View All Blogs</Link>
      </Button>
      <Button asChild className='gap-2'>
        <Link href='/blogs/new'>Write New Blog</Link>
      </Button>
    </div>
  )
}

export default ProfileActionButtons